from langgraph.prebuilt import create_react_agent
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
import json
from tools.tools import search_hcp, log_interaction, edit_latest_interaction, generate_summary, schedule_follow_up

# Attempt to load the model
try:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
except Exception as e:
    print(f"Warning: Could not initialize Groq LLM. Missing API Key? {e}")
    llm = None

tools_list = [search_hcp, log_interaction, edit_latest_interaction, generate_summary, schedule_follow_up]

system_prompt = """
You are a helpful CRM AI assistant for Healthcare Professionals (HCPs).
You have access to 5 tools:
1. search_hcp: Search for HCPs in the database.
2. log_interaction: Log a new interaction (pass fields directly as parameters).
3. edit_latest_interaction: Edit the most recently logged interaction.
4. generate_summary: Generate a summary of notes.
5. schedule_follow_up: Recommend follow-up actions.

CRITICAL RULES:
- When a user asks you to log an interaction, extract the structured data and call `log_interaction` with the appropriate fields (e.g. hcp_name, interaction_type, date (YYYY-MM-DD), time (HH:MM), attendees (array), topics_discussed (array), materials_shared (array)).
- If the user asks to correct or change a mistake, DO NOT guess an interaction ID. Call `edit_latest_interaction` with only the fields you want to update.
- If a tool returns an error, DO NOT call it again. Just output the final JSON and stop.
- Do NOT hallucinate data. If the user does not specify attendees, leave it empty or null (DO NOT put "John Doe").
- Once done, reply with a final JSON object wrapped in <json>...</json> representing the ENTIRE updated form state so the UI can update. DO NOT mention or announce the JSON in your friendly response text (e.g. do not say "Here is the JSON"). Just output it silently at the very end.
"""

if llm:
    agent = create_react_agent(llm, tools=tools_list, prompt=system_prompt)
else:
    agent = None
