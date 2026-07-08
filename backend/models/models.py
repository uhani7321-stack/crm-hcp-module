from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)
    hospital = Column(String)
    city = Column(String)

    interactions = relationship("Interaction", back_populates="hcp")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=True) # nullable because sometimes we just extract text without exact hcp match
    interaction_type = Column(String)
    date = Column(Date)
    time = Column(Time)
    attendees = Column(JSON) # Storing array as JSON
    topics_discussed = Column(JSON) # Storing array as JSON
    materials_shared = Column(JSON) # Storing array as JSON
    samples_distributed = Column(String)
    sentiment = Column(String)
    outcomes = Column(Text)
    follow_up_actions = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")
