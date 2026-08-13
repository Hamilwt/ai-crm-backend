from fastapi import APIRouter
from app.models import LeadModel
from app.database import lead_collection
from app.services import send_slack_notification

router = APIRouter()

@router.post("/leads/")
async def create_lead(lead: LeadModel):
    # 1. Save to MongoDB
    lead_dict = lead.model_dump()
    new_lead = await lead_collection.insert_one(lead_dict)
    
    # 2. Trigger the Slack notification (runs in the background)
    await send_slack_notification(lead.name, lead.company)
    
    return {"message": "Lead created and notification sent!", "id": str(new_lead.inserted_id)}

@router.get("/leads/")
async def get_leads():
    leads = []
    cursor = lead_collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        leads.append(document)
    return leads