def grade_email(email):
    if not email:
        return 0.0

    score = 0.0

    email = email.lower()

    if "hello" in email:
        score += 0.3

    if "interested" in email:
        score += 0.4

    if "thank you" in email:
        score += 0.3

    return min(score, 1.0)