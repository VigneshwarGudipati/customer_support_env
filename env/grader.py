def evaluate_response(response, task):
    response = response.lower()

    score = 0
    breakdown = {}

    # empathy
    if any(word in response for word in ["sorry", "understand"]):
        score += 3
        breakdown["empathy"] = True

    # correctness
    if any(word in response for word in task["expected"]):
        score += 3
        breakdown["correctness"] = True

    # helpfulness
    if "help" in response or "check" in response:
        score += 2
        breakdown["helpful"] = True

    # length
    if len(response) > 20:
        score += 2
        breakdown["length"] = True

    return score, breakdown