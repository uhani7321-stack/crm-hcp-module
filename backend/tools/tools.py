from langchain_core.tools import tool
from database.database import SessionLocal
from models.models import Interaction, HCP
from schemas.schemas import InteractionCreate
import json

@tool
def search_hcp(query: str) -> str:
    """Search existing Healthcare Professional records by name."""
    db = SessionLocal()
    try:
        hcps = db.query(HCP).filter(HCP.name.ilike(f"%{query}%")).all()
        if not hcps:
            return "No HCP found."
        return json.dumps([{"id": h.id, "name": h.name, "specialization": h.specialization} for h in hcps])
    finally:
        db.close()

from typing import Optional, List

@tool
def log_interaction(
    hcp_name: Optional[str] = None, interaction_type: Optional[str] = None, date: Optional[str] = None, time: Optional[str] = None,
    attendees: Optional[list] = None, topics_discussed: Optional[list] = None, materials_shared: Optional[list] = None,
    samples_distributed: Optional[str] = None, sentiment: Optional[str] = None, outcomes: Optional[str] = None, follow_up_actions: Optional[str] = None,
    summary: Optional[str] = None
) -> str:
    """Save interaction details into database. Pass the interaction fields as arguments."""
    db = SessionLocal()
    try:
        # Find HCP by name
        hcp_id = None
        if hcp_name:
            hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
            if hcp:
                hcp_id = hcp.id
                
        # Parse date and time if provided as strings
        parsed_date = None
        if date:
            try:
                from datetime import datetime
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                pass
                
        parsed_time = None
        if time:
            try:
                from datetime import datetime
                parsed_time = datetime.strptime(time, "%H:%M").time()
            except ValueError:
                pass
                
        data = {
            "hcp_id": hcp_id, "interaction_type": interaction_type, "date": parsed_date, "time": parsed_time,
            "attendees": attendees, "topics_discussed": topics_discussed, "materials_shared": materials_shared,
            "samples_distributed": samples_distributed, "sentiment": sentiment, "outcomes": outcomes, "follow_up_actions": follow_up_actions,
            "summary": summary
        }
        # filter out None
        data = {k: v for k, v in data.items() if v is not None}
        interaction = Interaction(**data)
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return f"Interaction logged with ID: {interaction.id}"
    except Exception as e:
        return f"Error logging interaction: {e}"
    finally:
        db.close()

@tool
def edit_latest_interaction(
    hcp_name: Optional[str] = None, interaction_type: Optional[str] = None, date: Optional[str] = None, time: Optional[str] = None,
    attendees: Optional[list] = None, topics_discussed: Optional[list] = None, materials_shared: Optional[list] = None,
    samples_distributed: Optional[str] = None, sentiment: Optional[str] = None, outcomes: Optional[str] = None, follow_up_actions: Optional[str] = None,
    summary: Optional[str] = None
) -> str:
    """Allow updating the most recently logged interaction. Pass only the fields you want to update."""
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).order_by(Interaction.id.desc()).first()
        if not interaction:
            return "Interaction not found."
        
        hcp_id = None
        if hcp_name:
            hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
            if hcp:
                hcp_id = hcp.id
                
        # Parse date and time if provided as strings
        parsed_date = None
        if date:
            try:
                from datetime import datetime
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                pass
                
        parsed_time = None
        if time:
            try:
                from datetime import datetime
                parsed_time = datetime.strptime(time, "%H:%M").time()
            except ValueError:
                pass
                
        updates = {
            "hcp_id": hcp_id, "interaction_type": interaction_type, "date": parsed_date, "time": parsed_time,
            "attendees": attendees, "topics_discussed": topics_discussed, "materials_shared": materials_shared,
            "samples_distributed": samples_distributed, "sentiment": sentiment, "outcomes": outcomes, "follow_up_actions": follow_up_actions,
            "summary": summary
        }
        for key, value in updates.items():
            if value is not None:
                setattr(interaction, key, value)
        db.commit()
        return f"Latest interaction updated."
    except Exception as e:
        return f"Error updating interaction: {e}"
    finally:
        db.close()

@tool
def generate_summary(text: str) -> str:
    """Generate a concise summary of the interaction using the LLM. Pass the raw text."""
    # In a real scenario, this might call an LLM directly, but since this is a tool called by the LLM, 
    # the LLM can just summarize it, or we use a separate small prompt here.
    return f"Summary generated: {text[:50]}..."

@tool
def schedule_follow_up(text: str) -> str:
    """Generate recommended follow-up actions based on the conversation."""
    if "samples" in text.lower() or "brochure" in text.lower():
        return "Follow up in 1 week to discuss samples/brochure."
    return "Schedule a routine follow-up meeting in 1 month."
