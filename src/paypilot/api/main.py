import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.paypilot.ai.openrouter_client import ask_ai

app = FastAPI(
    title="PayPilot AI API",
    description="AI-powered commerce and payment copilot",
    version="0.2.0",
)


class AIRequest(BaseModel):
    prompt: str


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "PayPilot AI API"}


@app.get("/")
def root():
    return {"message": "Welcome to PayPilot AI", "docs": "/docs"}


@app.post("/ai/assist")
def ai_assist(request: AIRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        answer, model = ask_ai(request.prompt)
        return {"answer": answer, "model": model}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenRouter returned HTTP {exc.response.status_code}.",
        ) from exc
    except (httpx.RequestError, RuntimeError, KeyError, IndexError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI request failed: {type(exc).__name__}",
        ) from exc
