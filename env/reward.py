def compute_reward(score):
    if score >= 8:
        return 10
    elif score >= 5:
        return 5
    else:
        return -5