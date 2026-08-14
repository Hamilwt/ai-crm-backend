def calculate_lead_score(email: str, company: str) -> float:
    """
    Calculates a probability score (0-100) of a lead closing based on data points.
    In a production app, this would route to a Scikit-Learn or PyTorch model.
    """
    score = 40.0  # Base probability score
    
    # Check for professional/corporate email domains
    free_email_providers = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]
    if not any(provider in email.lower() for provider in free_email_providers):
        score += 30.0  # Big bump for using a corporate email
        
    # Check if the company is an established entity
    corporate_identifiers = ["inc", "llc", "corp", "ltd", "technologies"]
    if any(identifier in company.lower() for identifier in corporate_identifiers):
        score += 20.0  # Bump for established companies
        
    return min(score, 99.9)  # Cap the maximum score at 99.9%