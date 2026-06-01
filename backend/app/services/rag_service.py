import json
import os
import pickle
import re

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "major_kb_modern_majors_v3.json"
)

VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")
INDEX_PATH = os.path.join(VECTOR_DIR, "major_index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "major_chunks.pkl")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class RAGService:
    def __init__(self):
        os.makedirs(VECTOR_DIR, exist_ok=True)

        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.index = None
        self.chunks = []

        if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            self.load_vector_store()
        else:
            self.build_vector_store()

    def load_knowledge_base(self):
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Knowledge base file not found: {DATA_PATH}")

        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("majors", [])

    def clean_text(self, value):
        if value is None:
            return ""

        text = str(value)
        text = text.replace("Paññāsāstra", "Pannasastra")
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def list_to_text(self, items):
        if not items:
            return ""

        cleaned = []

        for item in items:
            if isinstance(item, str):
                cleaned.append(self.clean_text(item))
            elif isinstance(item, dict):
                name = self.clean_text(item.get("name", ""))
                major = self.clean_text(item.get("major", ""))
                value = name or major or self.clean_text(item)
                cleaned.append(value)
            else:
                cleaned.append(self.clean_text(item))

        return ", ".join([x for x in cleaned if x])

    def universities_to_text(self, universities):
        lines = []

        for item in universities:
            name = self.clean_text(item.get("name", ""))
            faculty = self.clean_text(item.get("faculty", ""))
            evidence = self.clean_text(item.get("evidence", ""))

            if name:
                if faculty and evidence:
                    lines.append(f"- {name}, {faculty}. Evidence: {evidence}")
                elif faculty:
                    lines.append(f"- {name}, {faculty}")
                else:
                    lines.append(f"- {name}")

        return "\n".join(lines)

    def related_fields_to_text(self, related_fields):
        lines = []

        for field in related_fields:
            name = self.clean_text(field.get("name", ""))
            description = self.clean_text(field.get("description", ""))
            reason = self.clean_text(field.get("related_reason", ""))
            careers = self.list_to_text(field.get("possible_careers", []))
            keywords = self.list_to_text(field.get("keywords", []))

            if not name:
                continue

            line = f"- {name}"

            if description:
                line += f": {description}"

            if reason:
                line += f" Related reason: {reason}"

            if careers:
                line += f" Possible careers: {careers}."

            if keywords:
                line += f" Keywords: {keywords}."

            lines.append(line)

        return "\n".join(lines)

    def related_majors_to_text(self, related_majors):
        lines = []

        for item in related_majors:
            if isinstance(item, dict):
                major = self.clean_text(item.get("major", ""))
                macro = self.clean_text(item.get("macro_major", ""))
                reason = self.clean_text(item.get("relation_reason", ""))

                if major and macro and reason:
                    lines.append(f"- {major} ({macro}): {reason}")
                elif major and macro:
                    lines.append(f"- {major} ({macro})")
                elif major:
                    lines.append(f"- {major}")
            else:
                lines.append(f"- {self.clean_text(item)}")

        return "\n".join(lines)

    def source_references_to_text(self, source_references):
        lines = []

        for source in source_references:
            name = self.clean_text(source.get("source_name", ""))
            source_type = self.clean_text(source.get("source_type", ""))
            used_for = self.list_to_text(source.get("used_for", []))

            if name:
                lines.append(f"- {name} ({source_type}). Used for: {used_for}")

        return "\n".join(lines)

    def convert_major_to_text(self, major):
        universities = major.get("universities_in_cambodia", [])
        related_majors = major.get("related_majors", [])
        recommended_projects = major.get("recommended_projects", [])
        related_fields = major.get("related_fields", [])
        career_keywords = major.get("career_keywords", [])
        source_references = major.get("source_references", [])

        rag_metadata = major.get("rag_metadata", {})
        retrieval_keywords = rag_metadata.get("retrieval_keywords", [])

        base_text = f"""
Major: {self.clean_text(major.get("major", ""))}
Macro Major: {self.clean_text(major.get("macro_major", ""))}

Description:
{self.clean_text(major.get("description", ""))}

Prerequisites:
{self.list_to_text(major.get("prerequisites", []))}

Duration:
{self.clean_text(major.get("duration_years", ""))} years

Credits:
{self.clean_text(major.get("credits", ""))}

Possible Careers:
{self.list_to_text(major.get("possible_careers", []))}

Universities in Cambodia:
{self.universities_to_text(universities)}

Related Majors:
{self.related_majors_to_text(related_majors)}

Related Fields and Subfields:
{self.related_fields_to_text(related_fields)}

Career Keywords:
{self.list_to_text(career_keywords)}

Retrieval Keywords:
{self.list_to_text(retrieval_keywords)}

Recommended Projects:
{chr(10).join([f"- {self.clean_text(item)}" for item in recommended_projects])}

Source References:
{self.source_references_to_text(source_references)}
""".strip()

        search_text = self.clean_text(major.get("search_text", ""))

        if search_text:
            base_text += f"\n\nExtra Search Text:\n{search_text}"

        return base_text

    def build_chunks(self):
        majors = self.load_knowledge_base()
        chunks = []

        for major in majors:
            text = self.convert_major_to_text(major)

            chunks.append(
                {
                    "major": major.get("major", ""),
                    "macro_major": major.get("macro_major", ""),
                    "slug": major.get("slug", ""),
                    "text": text,
                    "raw": major,
                }
            )

        return chunks

    def build_vector_store(self):
        self.chunks = self.build_chunks()

        if not self.chunks:
            raise ValueError("No chunks found in knowledge base.")

        texts = [chunk["text"] for chunk in self.chunks]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = embeddings.astype(np.float32)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        faiss.write_index(self.index, INDEX_PATH)

        with open(CHUNKS_PATH, "wb") as file:
            pickle.dump(self.chunks, file)

        print("Vector store created successfully.")
        print(f"Total chunks: {len(self.chunks)}")
        print(f"Knowledge base file: {DATA_PATH}")

    def load_vector_store(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "rb") as file:
            self.chunks = pickle.load(file)

        print("Vector store loaded successfully.")
        print(f"Total chunks: {len(self.chunks)}")
        print(f"Knowledge base file: {DATA_PATH}")

    def retrieve(self, query, top_k=4):
        if not query:
            return []

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = query_embedding.astype(np.float32)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "score": float(score),
                    "major": chunk["major"],
                    "macro_major": chunk["macro_major"],
                    "slug": chunk["slug"],
                    "text": chunk["text"],
                    "raw": chunk["raw"],
                }
            )

        return results


rag_service = RAGService()