def calculate_priority(relationship_type, response_speed):

    base_score = 50

    if relationship_type == "family":
        base_score += 40

    if relationship_type == "romantic":
        base_score += 35

    if response_speed < 2:
        base_score += 10

    return base_score
