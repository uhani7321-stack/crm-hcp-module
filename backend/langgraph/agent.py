from langgraph.prebuilt import create_react_agent
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
import json
from tools.tools import search_hcp, log_interaction, edit_interaction, generate_summary, schedule_follow_up

# Attempt to load the model
try:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
except Exception as e:
    print(f"Warning: Could not initialize Groq LLM. Missing API Key? {e}")
    llm = None

tools_list = [search_hcp, log_interaction, edit_interaction, generate_summary, schedule_follow_up]

system_prompt = """
You are a helpful CRM AI assistant for Healthcare Professionals (HCPs).
You have access to 5 tools:
1. search_hcp: Search for HCPs in the database.
2. log_interaction: Log a new interaction (must provide a JSON string).
3. edit_interaction: Edit an existing interaction.
4. generate_summary: Generate a summary of notes.
5. schedule_follow_up: Recommend follow-up actions.

When a user asks you to log an interaction or provides interaction details, you should FIRST extract the structured data and then call `log_interaction` with a JSON string matching this schema:
{
    "hcp_name": "string or null",
    "interaction_type": "string",
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

Help the user by utilizing your tools, then give a friendly response!
To ensure the UI form updates, ALWAYS end your final response message with the raw JSON of the interaction state wrapped in a <json>...</json> tag block.
"""

if llm:
    agent = create_react_agent(llm, tools=tools_list, prompt=system_prompt)
else:
    agent = None
