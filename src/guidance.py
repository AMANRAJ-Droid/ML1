def generate_guidance(state, intensity, stress, energy, time_of_day, action, timing):

    steps = []
    explanation = ""

    # -------- 1. UNDERSTANDING --------
    if state == "anxious":
        explanation = "Your mind is overloaded"
    elif state == "sad":
        explanation = "Your emotional energy is low"
    elif state == "happy":
        explanation = "You're in a strong mental state"
    else:
        explanation = "You're slightly off balance"

    # -------- 2. CRITICAL CONDITIONS --------

    # 🚨 Burnout Case
    if stress >= 8 and energy <= 3:
        steps = [
            "Step 1: Pause immediately",
            "Step 2: Do 2-minute deep breathing",
            "Step 3: Avoid any heavy work",
            "Step 4: Take proper rest"
        ]
        final_action = "Recover first before doing anything else"

    # ⚡ Anxiety Regulation
    elif state == "anxious":
        steps = [
            "Step 1: Slow your breathing (box breathing)",
            "Step 2: Remove distractions",
            "Step 3: Focus on one simple task"
        ]
        final_action = "Stabilize your mind before proceeding"

    # 🌙 Night Recovery Flow
    elif time_of_day == "night" and state in ["sad", "anxious"]:
        steps = [
            "Step 1: Write down your thoughts",
            "Step 2: Disconnect from screens",
            "Step 3: Prepare for sleep calmly"
        ]
        final_action = "Let your mind settle before sleep"

    # 🚀 Peak Performance Mode
    elif state == "happy" and energy >= 7:
        steps = [
            "Step 1: Remove distractions",
            "Step 2: Define one clear goal",
            "Step 3: Start deep work session"
        ]
        final_action = "Use this peak state effectively"

    # 🔋 Low Energy Recovery
    elif energy <= 3:
        steps = [
            "Step 1: Take a short break",
            "Step 2: Do light movement",
            "Step 3: Resume with a small task"
        ]
        final_action = "Gradually rebuild energy"

    # ⚖️ Default Balanced Flow
    else:
        steps = [
            "Step 1: Pause and observe your state",
            "Step 2: Choose a small task",
            "Step 3: Move forward slowly"
        ]
        final_action = "Stay consistent with small actions"

    # -------- 3. TIMING --------
    timing_map = {
        "now": "right now",
        "within_15_min": "in the next 15 minutes",
        "later_today": "later today",
        "tonight": "tonight",
        "tomorrow_morning": "tomorrow morning"
    }

    timing_text = timing_map.get(timing, timing)

    # -------- 4. BUILD RESPONSE --------
    response = f"🧠 {explanation}.\n\n"

    for step in steps:
        response += f"{step}\n"

    response += f"\n🎯 {final_action}. Do this {timing_text}."

    return response