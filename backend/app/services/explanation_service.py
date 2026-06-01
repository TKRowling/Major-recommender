def generate_explanation(payload, macro_major):
    rules = {
        "Digital Technology": [
            ("Computer Skill", payload.get("computer_skill", 0), "Your computer-related skill profile supports technology majors."),
            ("Analytical Skill", payload.get("analytical_skill", 0), "Analytical strength is useful for data, software, and systems work."),
            ("Interests", payload.get("interests", []), "Your interests point toward digital and technology-focused fields."),
        ],
        "Education": [
            ("Communication Skill", payload.get("communication_skill", 0), "Communication is important for teaching, mentoring, and learning support roles."),
            ("Teamwork", payload.get("teamwork", 0), "Education work often needs collaboration and patience."),
            ("Interests", payload.get("interests", []), "Your interests align with learning and teaching environments."),
        ],
        "Financial Services": [
            ("Analytical Skill", payload.get("analytical_skill", 0), "Financial fields rely on analysis and careful judgment."),
            ("Logical Thinking", payload.get("logical_thinking", 0), "Logical thinking supports financial reasoning and decision-making."),
            ("Good At Subjects", payload.get("good_at_subjects", []), "Your stronger subjects support business and finance-related work."),
        ],
        "Business & Management": [
            ("Leadership", payload.get("leadership", 0), "Leadership is useful for management and entrepreneurial paths."),
            ("Communication Skill", payload.get("communication_skill", 0), "Business fields rely on presenting ideas and coordinating with people."),
            ("Interests", payload.get("interests", []), "Your interests suggest alignment with organization, strategy, or business growth."),
        ],
        "Creative & Hospitality": [
            ("Creativity", payload.get("creativity", 0), "Creativity is a strong fit for design, media, and hospitality-related work."),
            ("Hobbies", payload.get("hobbies", []), "Your hobbies suggest interest in expressive or people-facing activities."),
            ("Favorite Subjects", payload.get("favorite_subjects", []), "Your preferred subjects support creative or communication-focused learning."),
        ],
        "Engineering & Manufacturing": [
            ("Problem Solving", payload.get("problem_solving", 0), "Engineering paths benefit from structured problem solving."),
            ("Logical Thinking", payload.get("logical_thinking", 0), "Logical thinking is important for technical design and production work."),
            ("Good At Subjects", payload.get("good_at_subjects", []), "Your stronger technical subjects support engineering-related study."),
        ],
        "Agriculture & Natural Resources": [
            ("Interests", payload.get("interests", []), "Your interests indicate fit with environment, agriculture, or sustainability themes."),
            ("Good At Subjects", payload.get("good_at_subjects", []), "Relevant science subjects support this area."),
            ("Analytical Skill", payload.get("analytical_skill", 0), "Analytical skill helps with agricultural and environmental decision-making."),
        ],
        "Healthcare & Public Services": [
            ("Communication Skill", payload.get("communication_skill", 0), "Communication matters in care and service-oriented professions."),
            ("Teamwork", payload.get("teamwork", 0), "Healthcare and public services often require teamwork and coordination."),
            ("Interests", payload.get("interests", []), "Your interests suggest fit with care, health, or community support."),
        ],
    }

    selected = rules.get(macro_major, [
        ("Interests", payload.get("interests", []), "Your interests contributed to this recommendation."),
        ("Favorite Subjects", payload.get("favorite_subjects", []), "Your favorite subjects influenced the result."),
        ("Problem Solving", payload.get("problem_solving", 0), "Your skill profile helped shape this result."),
    ])

    explanation_items = []
    for feature_name, value, message in selected:
        if isinstance(value, list):
            detail = ", ".join(value[:3]) if value else "No specific items selected"
        else:
            detail = f"{value}/5"

        explanation_items.append({
            "feature": feature_name,
            "detail": detail,
            "message": message,
        })

    return explanation_items[:3]
