def decide_action(state, intensity, stress, energy, time):

    if stress > 7 and energy < 4:
        return "box_breathing", "now"

    if energy < 3 and time == "night":
        return "sleep", "now"

    if energy > 7 and intensity < 3:
        return "deep_work", "within_15_min"

    if state in ["anxious", "restless"]:
        return "grounding", "now"

    if state in ["sad", "low"]:
        return "movement", "within_15_min"

    return "light_planning", "later_today"