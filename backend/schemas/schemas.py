from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time, datetime

class HCPBase(BaseModel):
    name: str
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    city: Optional[str] = None

class HCPCreate(HCPBase):
    pass

class HCP(HCPBase):
    id: int
    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    hcp_id: Optional[int] = None
    interaction_type: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    attendees: Optional[List[str]] = []
    topics_discussed: Optional[List[str]] = []
    materials_shared: Optional[List[str]] = []
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    summary: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ExtractedDataResponse(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[List[str]] = []
    topics_discussed: Optional[List[str]] = []
    materials_shared: Optional[List[str]] = []
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    summary: Optional[str] = None
