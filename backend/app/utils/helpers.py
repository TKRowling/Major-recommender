MACRO_MAJORS = [
    "Agriculture & Natural Resources",
    "Business & Management",
    "Creative & Hospitality",
    "Digital Technology",
    "Education",
    "Engineering & Manufacturing",
    "Financial Services",
    "Healthcare & Public Services",
]


def safe_list(value):
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []
