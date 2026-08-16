from fastapi import APIRouter
from app.models import LeadModel, NoteModel
from app.database import lead_collection
from app.services import send_slack_notification
from app.ai_engine import calculate_lead_score, analyze_sentiment, get_next_best_action # <-- Notice the new import!
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
    sentiment = analyze_sentiment(note.text)
    result = await lead_collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {"sentiment_score": sentiment}}
    )
    if result.modified_count == 0:
        return {"error": "Lead not found"}
    return {"message": "Note analyzed!", "detected_sentiment": sentiment}

# --- NEW ENDPOINT BELOW ---
@router.get("/leads/{lead_id}/action")
async def recommend_action(lead_id: str):
    # 1. Fetch the lead from MongoDB
    lead = await lead_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        return {"error": "Lead not found"}
        
    # 2. Extract their current stats
    score = lead.get("lead_score", 0.0)
    sentiment = lead.get("sentiment_score", "NEUTRAL")
    
    # 3. Generate the AI recommendation
    action = get_next_best_action(score, sentiment)
    
    return {
        "lead_id": lead_id,
        "current_score": score,
        "current_sentiment": sentiment,
        "recommended_action": action
    }