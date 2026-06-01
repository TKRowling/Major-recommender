import json
import os

from app.utils.helpers import safe_list


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RULES_PATH = os.path.join(BASE_DIR, "rules", "macro_to_micro_mapping.json")

MACRO_MAJOR_ALIASES = {
    "Agriculture": "Agriculture & Natural Resources",
    "Advanced Manufacturing": "Engineering & Manufacturing",
    "Arts, Entertainment & Design": "Creative & Hospitality",
    "Construction": "Engineering & Manufacturing",
    "Energy & Natural Resources": "Agriculture & Natural Resources",
    "Healthcare & Human Services": "Healthcare & Public Services",
    "Hospitality, Events & Tourism": "Creative & Hospitality",
    "Management & Entrepreneurship": "Business & Management",
    "Marketing & Sales": "Business & Management",
    "Public Service & Safety": "Healthcare & Public Services",
    "Supply Chain & Transportation": "Business & Management",
}

FALLBACK_MAPPING = {
    "Agriculture & Natural Resources": [
        "Agronomy", "Animal Science", "Agribusiness", "Environmental Science", "Natural Resource Management"
    ],
    "Business & Management": [
        "Business Administration", "Entrepreneurship", "Management", "Marketing", "Accounting"
    ],
    "Creative & Hospitality": [
        "Graphic Design", "Media Production", "Animation", "Tourism Management", "Hospitality Management"
    ],
    "Digital Technology": [
        "Data Science", "Computer Science", "Cyber Security", "Software Engineering", "Information Technology"
    ],
    "Education": [
        "English Education", "Mathematics Education", "Science Education", "Primary Education", "Educational Management"
    ],
    "Engineering & Manufacturing": [
        "Mechanical Engineering", "Industrial Engineering", "Civil Engineering", "Architecture", "Automation Engineering"
    ],
    "Financial Services": [
        "Accounting", "Finance", "Banking", "Economics", "Auditing"
    ],
    "Healthcare & Public Services": [
        "Nursing", "Public Health", "Pharmacy", "Medical Laboratory", "Social Work"
    ],
}


def load_mapping():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    normalized = {}
    for key, values in raw.items():
        canonical_key = MACRO_MAJOR_ALIASES.get(key, key)
        normalized.setdefault(canonical_key, [])
        normalized[canonical_key].extend(values)

    for key, values in FALLBACK_MAPPING.items():
        normalized.setdefault(key, [])
        normalized[key].extend(values)

    deduped = {}
    for key, values in normalized.items():
        seen = set()
        deduped[key] = []
        for value in values:
            clean = str(value).strip()
            if clean and clean.lower() not in seen:
                deduped[key].append(clean)
                seen.add(clean.lower())

    return deduped


def recommend_micro_majors(macro_major, payload):
    mapping = load_mapping()
    candidates = mapping.get(macro_major, [])

    interests = [x.lower() for x in safe_list(payload.get("interests"))]
    hobbies = [x.lower() for x in safe_list(payload.get("hobbies"))]
    favorite_subjects = [x.lower() for x in safe_list(payload.get("favorite_subjects"))]
    good_at_subjects = [x.lower() for x in safe_list(payload.get("good_at_subjects"))]
    micro_major_input = str(payload.get("micro_major", "")).lower()

    scored = []

    for micro in candidates:
        score = 0
        micro_lower = micro.lower()

        if micro_major_input and micro_major_input in micro_lower:
            score += 5

        for text in interests + hobbies + favorite_subjects + good_at_subjects:
            for word in text.split():
                if word and word in micro_lower:
                    score += 1

        if macro_major == "Digital Technology" and payload.get("computer_skill", 0) >= 4:
            score += 2
        if macro_major == "Creative & Hospitality" and payload.get("creativity", 0) >= 4:
            score += 2
        if macro_major == "Business & Management" and payload.get("leadership", 0) >= 4:
            score += 2
        if macro_major == "Financial Services" and payload.get("analytical_skill", 0) >= 4:
            score += 2

        scored.append({"name": micro, "score": score})

    scored = sorted(scored, key=lambda x: x["score"], reverse=True)
    return scored[:3]
