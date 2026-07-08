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
    result = agent.invoke({"messages": [HumanMessage(content=request.message)], "extracted_data": {}})
    data = result.get("extracted_data", {})
    return data
