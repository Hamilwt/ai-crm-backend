from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LeadModel(BaseModel):
    name: str = Field(..., description="Full name of the lead")
    email: EmailStr = Field(..., description="Contact email")
    company: str = Field(..., description="Company name")
    status: str = Field(default="NEW")
    lead_score: Optional[float] = Field(default=None, description="AI predicted conversion probability")
    sentiment_score: Optional[str] = Field(default="NEUTRAL")
    days_since_last_contact: int = Field(default=0, description="Days since last communication")

class NoteModel(BaseModel):
    text: str = Field(..., description="The content of the note or email communication")