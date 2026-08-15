from fastapi import APIRouter
from app.models import LeadModel, NoteModel
from app.database import lead_collection
from app.services import send_slack_notification
from app.ai_engine import calculate_lead_score, analyze_sentiment
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/leads/")
async def create_lead(lead: LeadModel):
    generated_score = calculate_lead_score(lead.email, lead.company)
    lead.lead_score = generated_score
    
    lead_dict = lead.model_dump()
    new_lead = await lead_collection.insert_one(lead_dict)
    await send_slack_notification(lead.name, lead.company)
    
    return {"message": "Lead created!", "id": str(new_lead.inserted_id), "ai_score": generated_score}

@router.get("/leads/")
async def get_leads():
    leads = []
    cursor = lead_collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        leads.append(document)
    return leads

@router.post("/leads/{lead_id}/notes")
async def add_lead_note(lead_id: str, note: NoteModel):
    # 1. Analyze the sentiment of the note
    sentiment = analyze_sentiment(note.text)
    
    # 2. Update the lead's profile in MongoDB with the new sentiment
    result = await lead_collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {"sentiment_score": sentiment}}
    )
    
    if result.modified_count == 0:
        return {"error": "Lead not found"}
        
    return {"message": "Note analyzed!", "detected_sentiment": sentiment}