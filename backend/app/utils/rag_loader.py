import json
import os

from app.config import Config


def load_json_file(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_knowledge_base():
    kb_dir = os.path.join(Config.RAG_DIR, "knowledge_base")

    majors = load_json_file(os.path.join(kb_dir, "majors.json"))
    careers = load_json_file(os.path.join(kb_dir, "careers.json"))
    macro_majors = load_json_file(os.path.join(kb_dir, "macro_majors.json"))
    micro_majors = load_json_file(os.path.join(kb_dir, "micro_majors.json"))

    return {
        "majors": majors.get("majors", []) if isinstance(majors, dict) else majors,
        "careers": careers.get("careers", []) if isinstance(careers, dict) else careers,
        "macro_majors": macro_majors.get("macro_majors", []) if isinstance(macro_majors, dict) else macro_majors,
        "micro_majors": micro_majors.get("micro_majors", []) if isinstance(micro_majors, dict) else micro_majors,
    }