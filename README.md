# AI-First CRM HCP Module

## Overview
This project implements the "Log HCP Interaction" screen for a pharmaceutical CRM system. It allows field sales representatives to log interactions with Healthcare Professionals (HCPs) using either a structured form or an AI conversational assistant.

## Tech Stack
* **Frontend**: React.js, Redux Toolkit, Tailwind CSS, Axios
* **Backend**: Python, FastAPI, SQLAlchemy
* **AI Agent Framework**: LangGraph, Langchain
* **LLM**: Groq (`gemma2-9b-it`)
* **Database**: PostgreSQL (with SQLite fallback for local development)
* **Font**: Google Inter

## LangGraph AI Agent & Tools

### Role of the LangGraph Agent in Managing HCP Interactions
The LangGraph agent serves as the core orchestration engine that bridges natural language input with structured CRM data. When a sales representative types a conversational message (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure"), the LangGraph agent intercepts the message. It utilizes an LLM (`gemma2-9b-it` via Groq) to understand the context, extract relevant entities (HCP name, topics, sentiment, etc.), and map them to the structured fields required by the CRM database. The agent's role is to act as an intelligent assistant that reduces manual data entry, ensures data consistency, and dynamically selects tools to perform background tasks like summarizing the interaction or scheduling follow-ups.

### Defined Tools (Minimum of 5)
The LangGraph agent utilizes the following specific tools to assist in sales-related activities:

1. **Log Interaction**
   * **Purpose**: Captures and saves the interaction data into the database.
   * **Detail**: After the LLM extracts the entities (HCP Name, Interaction Type, Topics Discussed, Sentiment, etc.) from the natural language input, it maps them into a structured JSON format. This tool takes that structured data and inserts a new record into the `Interaction` database table, automatically linking it to the relevant HCP.

2. **Edit Interaction**
   * **Purpose**: Allows modification of previously logged data.
   * **Detail**: If a sales representative needs to append information (e.g., "I forgot to add that I gave him 5 samples"), the agent uses this tool to locate the specific interaction by ID and update the necessary fields in the database without overwriting the existing valid data.

3. **Search HCP**
   * **Purpose**: Retrieves existing Healthcare Professional records.
   * **Detail**: The agent uses this tool to query the database by the HCP's name or specialization to resolve the `hcp_id` before logging an interaction, ensuring the interaction is tied to the correct doctor in the CRM.

4. **Generate Summary**
   * **Purpose**: Generates a concise summary of the interaction.
   * **Detail**: Takes the raw transcription or long-form notes of the interaction and uses the LLM to distill it into a short, structured summary paragraph that is saved to the database for quick reading by managers.

5. **Schedule Follow-up**
   * **Purpose**: Suggests and schedules next steps.
   * **Detail**: Based on the outcomes of the interaction (e.g., if samples were requested or a future meeting was discussed), this tool generates recommended follow-up actions (like "Schedule meeting in 2 weeks") and prepares calendar reminders or tasks for the sales rep.

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Add your Groq API Key to `backend/.env`: `GROQ_API_KEY=your_key_here`
4. Run the server: `uvicorn main:app --reload` (Runs on port 8000)

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev` (Runs on port 5173)
