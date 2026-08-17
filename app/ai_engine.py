from textblob import TextBlob

def calculate_lead_score(email: str, company: str) -> float:
    score = 40.0
    free_email_providers = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]
    if not any(provider in email.lower() for provider in free_email_providers):
        score += 30.0
    corporate_identifiers = ["inc", "llc", "corp", "ltd", "technologies"]
    if any(identifier in company.lower() for identifier in corporate_identifiers):
        score += 20.0
    return min(score, 99.9)

def analyze_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "POSITIVE"
    elif analysis.sentiment.polarity < -0.1:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

def get_next_best_action(lead_score: float, sentiment: str) -> str:
    if lead_score >= 70 and sentiment == "NEGATIVE":
        return "URGENT: Call client immediately to resolve concerns and save this high-value deal."
    elif lead_score >= 70 and sentiment == "POSITIVE":
        return "Send the closing contract and premium onboarding materials."
    elif lead_score <= 40 and sentiment == "NEGATIVE":
        return "Drop lead to automated nurture campaign; save sales rep time."
    elif sentiment == "NEUTRAL":
        return "Send a personalized follow-up email with a relevant case study."
    else:
        return "Schedule a standard 15-minute discovery call."

def calculate_churn_risk(days_since_last_contact: int, sentiment: str) -> dict:
    """Predicts if a customer is at risk of leaving."""
    if days_since_last_contact > 14 and sentiment == "NEGATIVE":
        return {"risk_level": "CRITICAL RISK", "reason": "No contact in over 2 weeks with negative sentiment."}
    elif days_since_last_contact > 30:
        return {"risk_level": "HIGH RISK", "reason": "No contact in over 30 days. Relationship cooling."}
    elif sentiment == "NEGATIVE":
        return {"risk_level": "MODERATE RISK", "reason": "Recent negative communication detected."}
    else:
        return {"risk_level": "SAFE", "reason": "Recent contact and stable sentiment."}