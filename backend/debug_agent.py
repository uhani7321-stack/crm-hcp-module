import os
import json
import traceback
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage
from langgraph.agent import agent
from langgraph.agent import agent
try:
    for event in agent.stream(
        {"messages": [HumanMessage(content="Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure")]},
        {"recursion_limit": 5}
    ):
        print(event)
except Exception as e:
    print("EXCEPTION CAUGHT!")
    traceback.print_exc()
