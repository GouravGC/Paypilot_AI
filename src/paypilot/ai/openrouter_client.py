
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(prompt: str) -> tuple[str, str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openrouter/free")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing from .env")

    response = httpx.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are PayPilot AI, a helpful shopping assistant. "
                        "Help users clarify product needs and compare "
                        "shopping criteria. Never invent live prices, "
                        "stock, or product listings."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        },
        timeout=60.0,
    )

    response.raise_for_status()
    data = response.json()

    answer = data["choices"][0]["message"]["content"]
    actual_model = data.get("model", model)

    if not answer:
        raise RuntimeError("The AI returned an empty response.")

    return answer, actual_model
