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
    """Analyzes text sentiment and returns POSITIVE, NEGATIVE, or NEUTRAL."""
    analysis = TextBlob(text)
    # Polarity ranges from -1.0 (very negative) to 1.0 (very positive)
    if analysis.sentiment.polarity > 0.1:
        return "POSITIVE"
    elif analysis.sentiment.polarity < -0.1:
        return "NEGATIVE"
    else:
        return "NEUTRAL"