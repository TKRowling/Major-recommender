import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


load_dotenv()

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()
CLOUDFLARE_MODEL = os.getenv(
    "CLOUDFLARE_MODEL",
    "@cf/meta/llama-3.1-8b-instruct-fast",
).strip()
CLOUDFLARE_TIMEOUT = int(os.getenv("CLOUDFLARE_TIMEOUT", "60"))
CLOUDFLARE_MAX_TOKENS = int(os.getenv("CLOUDFLARE_MAX_TOKENS", "450"))
CLOUDFLARE_TEMPERATURE = float(os.getenv("CLOUDFLARE_TEMPERATURE", "0.1"))
CLOUDFLARE_GATEWAY_ID = os.getenv("CLOUDFLARE_GATEWAY_ID", "").strip()


class CloudflareAIError(RuntimeError):
    """Raised when Cloudflare Workers AI cannot generate a response."""


def is_cloudflare_configured() -> bool:
    return bool(CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN and CLOUDFLARE_MODEL)


def _extract_content(data: Dict[str, Any]) -> str:
    """Parse OpenAI-compatible or Cloudflare response formats safely."""
    choices = data.get("choices")

    if isinstance(choices, list) and choices:
        message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
        content = message.get("content")

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text") or part.get("content")
                    if text:
                        text_parts.append(str(text))
            return "\n".join(text_parts).strip()

    result = data.get("result")
    if isinstance(result, dict):
        response = result.get("response") or result.get("text")
        if isinstance(response, str):
            return response.strip()

    raise CloudflareAIError("Unexpected Cloudflare Workers AI response format.")


def generate_answer_with_cloudflare(
    question: str,
    context: str,
    session_id: Optional[str] = None,
) -> str:
    if not is_cloudflare_configured():
        raise CloudflareAIError(
            "Cloudflare Workers AI is not configured. Set CLOUDFLARE_ACCOUNT_ID, "
            "CLOUDFLARE_API_TOKEN, and CLOUDFLARE_MODEL."
        )

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/v1/chat/completions"
    )

    system_prompt = """
You are ChomNeanh AI, an academic major guidance chatbot for students in Cambodia.

Rules:
- Answer only using the provided knowledge base context.
- Do not invent universities, careers, subjects, duration, credits, or program details.
- If the context does not contain enough information, say the knowledge base does not have enough information.
- If the question is unrelated to majors, universities, careers, skills, prerequisites, or study guidance, say it is outside the scope of the knowledge base.
- If the user asks for a comparison, compare only the retrieved majors in the context.
- Keep the answer short, clear, and student-friendly.
""".strip()

    user_prompt = f"""
User question:
{question}

Retrieved knowledge base context:
{context}

Answer naturally based only on the retrieved context.
""".strip()

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    if CLOUDFLARE_GATEWAY_ID:
        headers["cf-aig-gateway-id"] = CLOUDFLARE_GATEWAY_ID

    if session_id:
        headers["x-session-affinity"] = session_id

    payload = {
        "model": CLOUDFLARE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": CLOUDFLARE_TEMPERATURE,
        "max_tokens": CLOUDFLARE_MAX_TOKENS,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=CLOUDFLARE_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise CloudflareAIError(f"Cloudflare Workers AI request failed: {exc}") from exc

    if response.status_code >= 400:
        raise CloudflareAIError(
            f"Cloudflare Workers AI error {response.status_code}: {response.text[:500]}"
        )

    data = response.json()
    return _extract_content(data)