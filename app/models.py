from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LeadModel(BaseModel):
    name: str = Field(..., description="Full name of the lead")
    email: EmailStr = Field(..., description="Contact email")
    company: str = Field(..., description="Company name")
    status: str = Field(default="NEW")
    lead_score: Optional[float] = Field(default=0.0)