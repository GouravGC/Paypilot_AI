
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first for better layer caching
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src/ ./src/

# Render provides PORT at runtime
EXPOSE 8000

CMD ["sh", "-c", "exec python -m uvicorn src.paypilot.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
