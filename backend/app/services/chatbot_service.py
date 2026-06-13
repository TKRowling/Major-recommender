import logging
import re

from dotenv import load_dotenv

from app.services.cloudflare_ai_service import (
    CloudflareAIError,
    generate_answer_with_cloudflare,
)
from app.services.rag_service import rag_service


load_dotenv()

logger = logging.getLogger(__name__)

OUT_OF_SCOPE_ANSWER = (
    "This question is outside the scope of my knowledge base. "
    "I can only answer questions about majors, universities, careers, "
    "skills, prerequisites, and study guidance."
)


class ChatbotService:
    def normalize(self, text):
        return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()

    def handle_general_message(self, question):
        q = self.normalize(question)

        greetings = {
            "hi", "hello", "hey", "yo", "good morning",
            "good afternoon", "good evening", "sousdey", "សួស្តី"
        }

        thanks = {
            "thank", "thanks", "thank you", "thank u", "thx",
            "ty", "ok", "okay", "alright", "great", "nice",
            "cool", "perfect", "awesome", "good", "got it"
        }

        goodbye = {"bye", "goodbye", "see you", "see ya"}

        help_patterns = [
            "what can you help", "what can you do", "how can you help",
            "help me", "what do you do", "who are you",
            "what is this chatbot", "tell me what you can do"
        ]

        if q in greetings:
            return (
                "Hi! I can help you with major recommendations, university suggestions, "
                "career paths, required subjects, skills, prerequisites, and study guidance."
            )

        if any(pattern in q for pattern in help_patterns):
            return (
                "I can help you with:\n"
                "- Explaining majors such as Data Science, Cyber Security, Accounting, Medicine, or Engineering\n"
                "- Recommending majors based on interests and skills\n"
                "- Suggesting universities in Cambodia\n"
                "- Showing possible careers for each major\n"
                "- Explaining prerequisites, duration, credits, and project ideas"
            )

        if q in thanks or any(word in q for word in ["thank", "thanks", "thx"]):
            return (
                "You're welcome. You can ask me about majors, universities, careers, "
                "skills, prerequisites, or study guidance anytime."
            )

        if q in goodbye:
            return "Goodbye! Good luck with your study and major selection."

        return None

    def extract_target_major_hint(self, question):
        q = self.normalize(question)

        aliases = {
            "computer science": [
                "computer science", "cs", "programming", "coding",
                "software", "information technology", "it"
            ],
            "information technology": [
                "information technology", "it", "computer science",
                "programming", "coding", "software"
            ],
            "data science": ["data science", "data analyst", "data analysis"],
            "artificial intelligence": ["artificial intelligence", "ai", "machine learning"],
            "cyber security": ["cyber security", "cybersecurity", "network security", "it security"],
            "software engineering": ["software engineering", "software development"],
            "business analytics": ["business analytics", "business analyst"],
            "digital marketing": ["digital marketing", "online marketing"],
            "financial technology": ["financial technology", "fintech"],
            "ux ui design": ["ux ui", "ux/ui", "ui design", "ux design"],
            "web and mobile development": ["web development", "mobile development", "mobile app"],
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
            keywords = self.normalize(
                " ".join(raw.get("rag_metadata", {}).get("retrieval_keywords", []))
            )

            score = float(item.get("score", 0))

            if target_hint and target_hint in major:
                score += 10

            for word in q.split():
                if len(word) >= 4 and (
                    word in major
                    or word in macro
                    or word in keywords
                    or word in description
                ):
                    score += 0.5

            reranked.append((score, item))

        reranked.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in reranked]

    def phrase_in_question(self, question, phrase):
        normalized_question = f" {self.normalize(question)} "
        normalized_phrase = self.normalize(phrase)

        if normalized_phrase == "ai":
            return re.search(r"\bai\b", normalized_question) is not None

        return normalized_phrase in normalized_question

    def select_best_chunks(self, question, retrieved_chunks, max_chunks=2):
        exact_map = {
            "data science": "Data Science",
            "cyber security": "Cyber Security",
            "cybersecurity": "Cyber Security",
            "artificial intelligence": "Artificial Intelligence",
            "ai": "Artificial Intelligence",
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

        requested_majors = []

        for keyword, target_major in exact_map.items():
            if self.phrase_in_question(question, keyword) and target_major not in requested_majors:
                requested_majors.append(target_major)

        selected = []

        for target_major in requested_majors:
            for chunk in retrieved_chunks:
                if chunk.get("major", "").lower() == target_major.lower():
                    selected.append(chunk)
                    break

        if selected:
            return selected[:max_chunks]

        return retrieved_chunks[:max_chunks]

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
            "technology", "english", "management", "economics", "compare",
            "difference", "different", "vs", "versus", "recommend", "suitable",
            "choose", "fit"
        ]

        has_education_keyword = any(word in q for word in education_keywords)
        top_score = float(retrieved_chunks[0].get("score", 0))

        return top_score < 0.35 and not has_education_keyword

    def build_context(self, retrieved_chunks):
        context_blocks = []

        for index, item in enumerate(retrieved_chunks, start=1):
            raw = item["raw"]
            universities = raw.get("universities_in_cambodia", [])
            related_majors = raw.get("related_majors", [])
            projects = raw.get("recommended_projects", [])
            related_fields = raw.get("related_fields", [])
            retrieval_keywords = raw.get("rag_metadata", {}).get("retrieval_keywords", [])

            university_text = "\n".join([
                f"- {u.get('name', '')}, {u.get('faculty', '')}. Evidence: {u.get('evidence', '')}"
                for u in universities[:5]
            ])

            related_text = ", ".join([
                r.get("major", "") if isinstance(r, dict) else str(r)
                for r in related_majors[:5]
            ])

            related_field_text = "\n".join([
                f"- {field.get('name', '')}: {field.get('description', '')}"
                for field in related_fields[:5]
            ])

            project_text = "\n".join([f"- {p}" for p in projects[:5]])

            context = f"""
Source {index}
Major: {raw.get("major", "")}
Macro Major: {raw.get("macro_major", "")}
Description: {raw.get("description", "")}
Prerequisites: {", ".join(raw.get("prerequisites", []))}
Duration: {raw.get("duration_years", "")} years
Credits: {raw.get("credits", "")}
Possible Careers: {", ".join(raw.get("possible_careers", []))}
Retrieval Keywords: {", ".join(retrieval_keywords[:15])}

Universities in Cambodia:
{university_text}

Related Majors:
{related_text}

Related Fields:
{related_field_text}

Recommended Projects:
{project_text}
""".strip()

            context_blocks.append(context)

        return "\n\n---\n\n".join(context_blocks)

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

    def generate_comparison_fallback(self, retrieved_chunks):
        if len(retrieved_chunks) < 2:
            return None

        first = retrieved_chunks[0]["raw"]
        second = retrieved_chunks[1]["raw"]

        return f"""
Here is the difference between {first.get("major", "")} and {second.get("major", "")}:

{first.get("major", "")}
- Field: {first.get("macro_major", "")}
- Focus: {first.get("description", "")}
- Possible careers: {", ".join(first.get("possible_careers", [])[:4])}

{second.get("major", "")}
- Field: {second.get("macro_major", "")}
- Focus: {second.get("description", "")}
- Possible careers: {", ".join(second.get("possible_careers", [])[:4])}
""".strip()

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

            return (
                f"For {major}, the knowledge base lists these universities in Cambodia:\n\n"
                + "\n".join(lines)
            )

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
            return (
                f"For {major}, possible career paths include:\n\n"
                + "\n".join([f"- {career}" for career in careers])
            )

        if question_type == "projects":
            return (
                f"For {major}, recommended project ideas include:\n\n"
                + "\n".join([f"- {project}" for project in projects[:5]])
            )

        return f"""
The most relevant major is {major} ({macro}).

{description}

Main details:
- Prerequisites: {prerequisites}
- Duration: {duration} years
- Credits: {credits}
- Possible careers: {", ".join(careers[:4])}
""".strip()

    def known_major_names(self):
        return [
            "Data Science",
            "Artificial Intelligence",
            "Cyber Security",
            "Software Engineering",
            "Computer Science / Information Technology",
            "Information Technology",
            "Business Analytics",
            "Accounting",
            "Banking and Finance",
            "Digital Marketing",
            "Financial Technology",
            "Medicine",
            "Pharmacy",
            "Civil Engineering",
            "Tourism",
            "English",
            "Law",
            "UX/UI Design",
            "Web and Mobile Development",
            "Cloud Computing",
            "Network Engineering",
        ]

    def find_last_major_from_history(self, history):
        if not isinstance(history, list):
            return None

        major_names = self.known_major_names()

        for message in reversed(history):
            content = str(message.get("content", "")).lower()

            for major in major_names:
                if major.lower() in content:
                    return major

        return None

    def is_follow_up_question(self, question):
        q = self.normalize(question)

        follow_up_words = [
            "that", "it", "this", "those", "them",
            "the previous", "above", "last one",
            "for that", "about that"
        ]

        return any(word in q for word in follow_up_words)

    def resolve_follow_up_question(self, question, history):
        if not self.is_follow_up_question(question):
            return question

        last_major = self.find_last_major_from_history(history)

        if not last_major:
            return question

        q = question.lower()

        if any(word in q for word in ["career", "job", "work", "become"]):
            return f"What are the possible careers for {last_major}?"

        if any(word in q for word in ["university", "universities", "school", "study"]):
            return f"Which universities in Cambodia offer {last_major}?"

        if any(word in q for word in ["project", "assignment", "portfolio"]):
            return f"What projects are recommended for {last_major}?"

        if any(word in q for word in ["subject", "prerequisite", "requirement"]):
            return f"What are the prerequisites for {last_major}?"

        return f"{question} about {last_major}"

    def answer_question(self, question, history=None, session_id=None):
        history = history or []

        general_answer = self.handle_general_message(question)

        if general_answer:
            return {"answer": general_answer}

        resolved_question = self.resolve_follow_up_question(question, history)

        retrieved_chunks = rag_service.retrieve(resolved_question, top_k=10)

        if self.is_out_of_scope(resolved_question, retrieved_chunks):
            return {"answer": OUT_OF_SCOPE_ANSWER}

        retrieved_chunks = self.rerank_chunks(resolved_question, retrieved_chunks)
        final_chunks = self.select_best_chunks(resolved_question, retrieved_chunks)

        try:
            context = self.build_context(final_chunks)
            answer = generate_answer_with_cloudflare(
                question=resolved_question,
                context=context,
                session_id=session_id,
            )

            if not answer or len(answer.strip()) < 20:
                answer = self.generate_fallback_answer(resolved_question, final_chunks)

        except Exception as exc:
            logger.warning(
                "Cloudflare generation failed; using deterministic fallback: %s",
                exc,
            )

            if any(word in resolved_question.lower() for word in ["difference", "different", "compare", "vs", "versus"]):
                answer = (
                    self.generate_comparison_fallback(final_chunks)
                    or self.generate_fallback_answer(resolved_question, final_chunks)
                )
            else:
                answer = self.generate_fallback_answer(resolved_question, final_chunks)

        return {"answer": answer}


chatbot_service = ChatbotService()