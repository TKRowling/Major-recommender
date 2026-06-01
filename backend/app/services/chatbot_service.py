import os
import re
import requests
from dotenv import load_dotenv

from app.services.rag_service import rag_service


load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class ChatbotService:
    def normalize(self, text):
        return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()

    def extract_target_major_hint(self, question):
        q = self.normalize(question)

        aliases = {
            "computer science": ["computer science", "cs", "programming", "coding", "software", "information technology", "it"],
            "information technology": ["information technology", "it", "computer science", "programming", "coding", "software"],
            "accounting": ["accounting", "accountant", "audit", "auditing"],
            "banking and finance": ["finance", "banking", "bank", "financial"],
            "english": ["english"],
            "tourism": ["tourism", "travel", "tour guide"],
            "law": ["law", "legal", "court"],
            "medicine": ["medicine", "doctor", "medical"],
            "pharmacy": ["pharmacy", "drug", "pharmacology"],
            "civil engineering": ["civil engineering", "construction", "building"],
        }

        for canonical, terms in aliases.items():
            if any(term in q for term in terms):
                return canonical

        return None

    def rerank_chunks(self, question, chunks):
        q = self.normalize(question)
        target_hint = self.extract_target_major_hint(question)

        reranked = []

        for item in chunks:
            raw = item["raw"]
            major = self.normalize(raw.get("major", ""))
            macro = self.normalize(raw.get("macro_major", ""))
            description = self.normalize(raw.get("description", ""))
            keywords = self.normalize(" ".join(raw.get("rag_metadata", {}).get("retrieval_keywords", [])))

            score = float(item.get("score", 0))

            if target_hint and target_hint in major:
                score += 10

            if target_hint in ["computer science", "information technology"]:
                if "computer science" in major or "information technology" in major:
                    score += 10
                if "digital technology" in macro:
                    score += 2
                if any(term in description for term in ["software", "database", "network", "systems"]):
                    score += 2

            if target_hint in ["computer science", "information technology"]:
                if any(wrong in major for wrong in ["english", "tourism", "law", "history", "khmer"]):
                    score -= 8

            for word in q.split():
                if len(word) >= 4 and (word in major or word in keywords or word in description):
                    score += 0.5

            reranked.append((score, item))

        reranked.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in reranked]

    def select_best_chunk(self, question, retrieved_chunks):
        q = f" {question.lower()} "

        exact_map = {
            "data science": "Data Science",
            "cyber security": "Cyber Security",
            "cybersecurity": "Cyber Security",
            "artificial intelligence": "Artificial Intelligence",
            " ai ": "Artificial Intelligence",
            "software engineering": "Software Engineering",
            "cloud computing": "Cloud Computing",
            "network engineering": "Network Engineering",
            "business analytics": "Business Analytics",
            "digital marketing": "Digital Marketing",
            "financial technology": "Financial Technology",
            "fintech": "Financial Technology",
            "ux/ui": "UX/UI Design",
            "ui design": "UX/UI Design",
            "ux design": "UX/UI Design",
            "web development": "Web and Mobile Development",
            "mobile development": "Web and Mobile Development",
        }

        for keyword, target_major in exact_map.items():
            if keyword in q:
                for chunk in retrieved_chunks:
                    if chunk.get("major", "").lower() == target_major.lower():
                        return [chunk]

        return retrieved_chunks[:2]

    def is_out_of_scope(self, question, retrieved_chunks):
        if not retrieved_chunks:
            return True

        q = question.lower()

        education_keywords = [
            "major", "university", "universities", "career", "job", "subject", "study",
            "prerequisite", "project", "skill", "degree", "school", "college",
            "data science", "cyber security", "cybersecurity", "ai", "software",
            "business", "accounting", "finance", "medicine", "engineering", "law",
            "marketing", "design", "tourism", "agriculture", "health", "computer",
            "technology", "english", "management", "economics"
        ]

        has_education_keyword = any(word in q for word in education_keywords)
        top_score = float(retrieved_chunks[0].get("score", 0))

        if top_score < 0.35 and not has_education_keyword:
            return True

        return False

    def build_context(self, retrieved_chunks):
        context_blocks = []

        for index, item in enumerate(retrieved_chunks, start=1):
            raw = item["raw"]

            universities = raw.get("universities_in_cambodia", [])
            related_majors = raw.get("related_majors", [])
            projects = raw.get("recommended_projects", [])

            university_text = "\n".join([
                f"- {u.get('name', '')}, {u.get('faculty', '')}. Evidence: {u.get('evidence', '')}"
                for u in universities[:4]
            ])

            related_text = ", ".join([
                r.get("major", "") if isinstance(r, dict) else str(r)
                for r in related_majors[:5]
            ])

            project_text = "\n".join([f"- {p}" for p in projects[:4]])

            context = f"""
Source {index}
Major: {raw.get("major", "")}
Macro Major: {raw.get("macro_major", "")}
Description: {raw.get("description", "")}
Prerequisites: {", ".join(raw.get("prerequisites", []))}
Duration: {raw.get("duration_years", "")} years
Credits: {raw.get("credits", "")}
Possible Careers: {", ".join(raw.get("possible_careers", []))}

Universities in Cambodia:
{university_text}

Related Majors:
{related_text}

Recommended Projects:
{project_text}
""".strip()

            context_blocks.append(context)

        return "\n\n---\n\n".join(context_blocks)

    def generate_answer_with_ollama(self, question, context):
        system_prompt = """
You are ChomNeanh AI, an academic major guidance chatbot for students in Cambodia.

Rules:
- Answer only using the provided knowledge base context.
- Do not invent universities, careers, subjects, duration, credits, or program details.
- If the question is unrelated to majors, universities, careers, skills, prerequisites, or study guidance, say it is outside the scope of the knowledge base.
- Use Source 1 as the main source.
- Keep the answer short and clear.
""".strip()

        user_prompt = f"""
User question:
{question}

Retrieved knowledge base context:
{context}

Answer naturally based only on the context.
""".strip()

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 180,
            },
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=45,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.text}")

        return response.json().get("message", {}).get("content", "").strip()

    def detect_question_type(self, question):
        q = question.lower()

        if any(x in q for x in ["university", "universities", "school", "offer", "study"]):
            return "universities"

        if any(x in q for x in ["what is", "what's", "define", "meaning"]):
            return "definition"

        if any(x in q for x in ["career", "job", "work", "become"]):
            return "careers"

        if any(x in q for x in ["project", "assignment", "portfolio"]):
            return "projects"

        if any(x in q for x in ["recommend", "fit", "suitable", "best", "choose"]):
            return "recommendation"

        return "general"

    def university_lines(self, universities):
        lines = []

        for u in universities[:5]:
            name = str(u.get("name", "")).strip()
            faculty = str(u.get("faculty", "")).strip()

            if name and faculty:
                lines.append(f"- {name} — {faculty}")
            elif name:
                lines.append(f"- {name}")

        return lines

    def generate_fallback_answer(self, question, retrieved_chunks):
        question_type = self.detect_question_type(question)
        top = retrieved_chunks[0]["raw"]

        major = top.get("major", "")
        macro = top.get("macro_major", "")
        description = top.get("description", "")
        prerequisites = ", ".join(top.get("prerequisites", []))
        duration = top.get("duration_years", "")
        credits = top.get("credits", "")
        careers = top.get("possible_careers", [])
        universities = top.get("universities_in_cambodia", [])
        projects = top.get("recommended_projects", [])

        if question_type == "universities":
            lines = self.university_lines(universities)

            if not lines:
                return f"The knowledge base does not list universities for {major}."

            return f"""
For {major}, the knowledge base lists these universities in Cambodia:

{chr(10).join(lines)}
""".strip()

        if question_type == "definition":
            return f"""
{major} is a major under {macro}.

{description}

Main details:
- Prerequisites: {prerequisites}
- Duration: {duration} years
- Credits: {credits}
- Possible careers: {", ".join(careers[:4])}
""".strip()

        if question_type == "careers":
            return f"""
For {major}, possible career paths include:

{chr(10).join([f"- {career}" for career in careers])}
""".strip()

        if question_type == "projects":
            return f"""
For {major}, recommended project ideas include:

{chr(10).join([f"- {project}" for project in projects[:5]])}
""".strip()

        return f"""
The most relevant major is {major} ({macro}).

{description}

Main details:
- Prerequisites: {prerequisites}
- Duration: {duration} years
- Credits: {credits}
- Possible careers: {", ".join(careers[:4])}
""".strip()

    def answer_question(self, question):
        retrieved_chunks = rag_service.retrieve(question, top_k=10)

        if self.is_out_of_scope(question, retrieved_chunks):
            return {
                "answer": (
                    "This question is outside the scope of my knowledge base. "
                    "I can only answer questions about majors, universities, careers, "
                    "skills, prerequisites, and study guidance."
                )
            }

        retrieved_chunks = self.rerank_chunks(question, retrieved_chunks)
        final_chunks = self.select_best_chunk(question, retrieved_chunks)

        try:
            context = self.build_context(final_chunks)
            answer = self.generate_answer_with_ollama(question, context)

            if not answer or len(answer.strip()) < 20:
                answer = self.generate_fallback_answer(question, final_chunks)

        except Exception:
            answer = self.generate_fallback_answer(question, final_chunks)

        return {
            "answer": answer
        }


chatbot_service = ChatbotService()