import os
import httpx
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

async def send_slack_notification(lead_name: str, lead_company: str):
    if not SLACK_WEBHOOK_URL:
        print("Slack webhook URL not found in .env")
        return
        
    message = {
        "text": f"🚀 *New Lead Alert!*\n*Name:* {lead_name}\n*Company:* {lead_company}\n_Log into the CRM to view details._"
    }
    
    # We use try/except so if Slack is down, your CRM doesn't crash
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(SLACK_WEBHOOK_URL, json=message)
            print(f"Slack API Response: {response.status_code}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")