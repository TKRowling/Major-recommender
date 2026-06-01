def micro_major_bonus_rules(macro_major, payload):
    bonus = 0

    if macro_major == "Digital Technology" and payload.get("computer_skill", 0) >= 4:
        bonus += 2

    if macro_major == "Financial Services" and payload.get("analytical_skill", 0) >= 4:
        bonus += 2

    if macro_major == "Arts, Entertainment & Design" and payload.get("creativity", 0) >= 4:
        bonus += 2

    if macro_major == "Management & Entrepreneurship" and payload.get("leadership", 0) >= 4:
        bonus += 2

    return bonus