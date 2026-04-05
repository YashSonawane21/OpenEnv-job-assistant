"""
LinkedIn Profile Grader
Evaluates LinkedIn profile completeness and quality:
- Profile completeness (photo, headline, bio)
- Keyword optimization
- Professional tone
- Call-to-action/contact info
Scores: 0.0 - 1.0
"""


def grade_linkedin_profile(profile_data: str) -> float:
    """
    Grade a LinkedIn profile based on completeness and quality.
    
    Args:
        profile_data: Profile information (can contain photo mention, headline, bio, etc.)
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if not profile_data or len(profile_data.strip()) == 0:
        return 0.0

    score = 0.0
    profile_lower = profile_data.lower()

    # Check for professional photo mention (0.15)
    if any(photo_indicator in profile_lower for photo_indicator in [
        "photo", "headshot", "profile picture", "image"
    ]):
        score += 0.15

    # Check for professional headline (0.2)
    if any(title_keyword in profile_lower for title_keyword in [
        "engineer", "developer", "analyst", "manager", "specialist", 
        "consultant", "architect", "lead", "senior"
    ]):
        score += 0.2

    # Check for detailed bio/summary (0.25)
    if len(profile_data.strip()) > 100:
        score += 0.15
    if len(profile_data.strip()) > 200:
        score += 0.1

    # Check for skills mentioned (0.15)
    if any(skills_indicator in profile_lower for skills_indicator in [
        "skills", "proficiencies", "expertise", "tools", "technologies",
        "python", "java", "javascript", "sql", "react", "node"
    ]):
        score += 0.15

    # Check for experience details (0.15)
    if any(exp_indicator in profile_lower for exp_indicator in [
        "experience", "worked", "led", "managed", "built", "developed",
        "years", "company", "role", "position"
    ]):
        score += 0.15

    # Check for contact/call-to-action (0.1)
    if any(cta in profile_lower for cta in [
        "contact", "email", "message", "reach out", "connect", "linkedin.com"
    ]):
        score += 0.1

    # Check for recommendations/endorsements mention (0.05)
    if any(social in profile_lower for social in ["recommendation", "endorsement", "verified"]):
        score += 0.05

    return min(score, 1.0)
