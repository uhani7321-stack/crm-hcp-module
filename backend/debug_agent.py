import os
import json
import traceback
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.agent import agent
from langgraph.agent import agent
try:
    for event in agent.stream(
        {"messages": [
            HumanMessage(content="I just had a 45-minute Meeting with Dr. Sarah Jenkins today at 2:00 PM. We discussed the Phase 3 trial results for OncoBoost. She seemed a bit neutral about it. I gave her the clinical trial summary brochure."),
            AIMessage(content='<json>{"attendees": [], "date": "2024-02-20", "hcp_name": "Dr. Sarah Jenkins", "interaction_type": "Meeting", "materials_shared": ["clinical trial summary brochure"], "sentiment": "neutral", "time": "14:00", "topics_discussed": ["OncoBoost Phase 3 trial results"]}</json>'),
            HumanMessage(content="the sentiment was positive")
        ]},
        {"configurable": {"thread_id": "1"}, "recursion_limit": 5}
    ):
        print(event)
except Exception as e:
    print("EXCEPTION CAUGHT!")
    traceback.print_exc()
