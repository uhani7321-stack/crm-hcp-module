from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.models import Interaction, HCP
from schemas.schemas import InteractionCreate, Interaction as InteractionSchema, ChatRequest, ExtractedDataResponse
from langgraph.agent import agent
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/interactions", response_model=InteractionSchema)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/interactions", response_model=List[InteractionSchema])
def get_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Interaction).offset(skip).limit(limit).all()

@router.post("/ai/extract")
def extract_from_chat(request: ChatRequest):
    try:
        try:
            result = agent.invoke(
                {"messages": [HumanMessage(content=request.message)]},
                config={"configurable": {"thread_id": "1"}}
            )
        except Exception as e:
            import traceback
            return {"summary": f"LLM Error: {str(e)} - {traceback.format_exc()}", "tools_called": []}
        
        # Extract which tools were called during this turn
        tools_called = []
        for msg in result["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tools_called.append(tool_call.get('name'))
                    
        # The last message is the AI's response
        final_message = result["messages"][-1].content
        if not isinstance(final_message, str):
            final_message = str(final_message)
        
        # Try to find the JSON block inside <json> tags or markdown
        data = {}
        json_str = ""
        if "<json>" in final_message and "</json>" in final_message:
            json_str = final_message.split("<json>")[1].split("</json>")[0].strip()
        elif "```json" in final_message and "```" in final_message.split("```json")[1]:
            json_str = final_message.split("```json")[1].split("```")[0].strip()
            
        if json_str:
            try:
                import json
                data = json.loads(json_str)
            except:
                pass
        
        # Clean the final message to remove the json blocks before sending to UI
        clean_message = final_message
        if "<json>" in clean_message:
            clean_message = clean_message.split("<json>")[0].strip()
        elif "```json" in clean_message:
            clean_message = clean_message.split("```json")[0].strip()
            
        data["summary"] = clean_message
        data["tools_called"] = tools_called
        
        return data
    except Exception as e:
        import traceback
        return {"summary": f"Server Logic Error: {str(e)} - {traceback.format_exc()}", "tools_called": []}
