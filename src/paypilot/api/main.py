
import os
import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from channel3_sdk import Channel3

from src.paypilot.ai.openrouter_client import ask_ai

app = FastAPI(
    title="PayPilot AI API",
    description="AI-powered commerce and payment copilot",
    version="0.3.0",
)


class AIRequest(BaseModel):
    prompt: str


class ProductSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=300)
    limit: int = Field(default=5, ge=1, le=10)


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


@app.post("/products/search")
def search_products(request: ProductSearchRequest):
    api_key = os.getenv("CHANNEL3_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="CHANNEL3_API_KEY is not configured.",
        )

    try:
        client = Channel3(api_key=api_key)
        results = client.products.search(
            query=request.query,
            limit=request.limit,
        )

        products = []
        for product in results:
            images = getattr(product, "images", None) or []
            offers = getattr(product, "offers", None) or []
            brands = getattr(product, "brands", None) or []
            ratings = getattr(product, "ratings", None)

            offer = offers[0] if offers else None
            price = getattr(offer, "price", None) if offer else None

            products.append({
                "id": getattr(product, "id", ""),
                "title": getattr(product, "title", "Unknown product"),
                "brand": getattr(brands[0], "name", "") if brands else "",
                "description": getattr(product, "description", "") or "",
                "image": getattr(images[0], "url", "") if images else "",
                "price": getattr(price, "price", None) if price else None,
                "currency": getattr(price, "currency", "") if price else "",
                "retailer": getattr(offer, "domain", "") if offer else "",
                "availability": getattr(offer, "availability", "") if offer else "",
                "buy_url": getattr(offer, "url", "") if offer else "",
                "rating": ratings.get("value") if isinstance(ratings, dict) else None,
                "rating_count": ratings.get("count") if isinstance(ratings, dict) else None,
                "features": getattr(product, "key_features", []) or [],
            })

        return {"query": request.query, "count": len(products), "products": products}

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Channel3 search failed: {type(exc).__name__}: {str(exc)[:300]}",
        ) from exc
