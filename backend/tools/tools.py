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

@tool
def log_interaction(interaction_data_json: str) -> str:
    """Save interaction details into database. Provide JSON string with interaction fields."""
    db = SessionLocal()
    try:
        data = json.loads(interaction_data_json)
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
def edit_interaction(interaction_id: int, updates_json: str) -> str:
    """Allow updating previously logged interaction."""
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return "Interaction not found."
        updates = json.loads(updates_json)
        for key, value in updates.items():
            setattr(interaction, key, value)
        db.commit()
        return f"Interaction {interaction_id} updated."
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
