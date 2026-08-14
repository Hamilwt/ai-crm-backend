from fastapi import APIRouter
from app.models import LeadModel
from app.database import lead_collection
from app.services import send_slack_notification
from app.ai_engine import calculate_lead_score

router = APIRouter()

@router.post("/leads/")
async def create_lead(lead: LeadModel):
    # 1. AI Analytics Engine: Calculate the lead score
    generated_score = calculate_lead_score(lead.email, lead.company)
    lead.lead_score = generated_score
    
    # 2. Save to MongoDB
    lead_dict = lead.model_dump()
    new_lead = await lead_collection.insert_one(lead_dict)
    
    # 3. Trigger the Slack notification
    await send_slack_notification(lead.name, lead.company)
    
    return {
        "message": "Lead created and scored!", 
        "id": str(new_lead.inserted_id),
        "ai_score": generated_score
    }

@router.get("/leads/")
async def get_leads():
    leads = []
    cursor = lead_collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        leads.append(document)
    return leads