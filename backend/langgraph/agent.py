from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
import json

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    extracted_data: dict

def create_agent():
    # Attempt to load the model. Ensure GROQ_API_KEY is in env
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    except Exception as e:
        print(f"Warning: Could not initialize Groq LLM. Missing API Key? {e}")
        llm = None
    
    def extract_information(state: AgentState):
        if not llm:
            return {"extracted_data": {"summary": "LLM not configured. Missing GROQ_API_KEY."}}
            
        prompt = """
        Extract structured information from the following HCP interaction log.
        Return ONLY a JSON object matching this schema exactly. Do not output anything else like markdown blocks or conversational text. Just raw JSON.
        
        {
          "hcp_name": "string or null",
          "interaction_type": "string (Meeting, Call, Email, Conference)",
          "date": "string YYYY-MM-DD",
          "time": "string HH:MM",
          "attendees": ["list of strings"],
          "topics_discussed": ["list of strings"],
          "materials_shared": ["list of strings"],
          "samples_distributed": "string or null",
          "sentiment": "string (Positive, Neutral, Negative)",
          "outcomes": "string or null",
          "follow_up_actions": "string or null",
          "summary": "string"
        }
        """
        user_msg = state['messages'][-1].content
        try:
            response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=user_msg)])
            content = response.content
        except Exception as e:
            error_msg = str(e)
            print(f"LLM Invoke Error: {error_msg}")
            if "401" in error_msg or "Invalid API Key" in error_msg:
                return {"extracted_data": {"summary": "Missing GROQ_API_KEY"}}
            return {"extracted_data": {"summary": f"LLM Error: {error_msg}"}}
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        try:
            data = json.loads(content)
        except Exception as e:
            print(f"Failed to parse JSON: {content}")
            data = {}
            
        return {"extracted_data": data}
        
    workflow = StateGraph(AgentState)
    workflow.add_node("extract", extract_information)
    workflow.set_entry_point("extract")
    workflow.add_edge("extract", END)
    
    return workflow.compile()

agent = create_agent()
