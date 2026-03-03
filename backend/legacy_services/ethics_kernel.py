def evaluate_safe_response(trust_score, tone_score, risk_score=0):

    # Emotional safety first
    if tone_score < 0.35:
        return True

    # High trust → more freedom
    if trust_score > 0.4:
        return True

    # Risk protection
    if risk_score > 0.4:
        return False

    return True