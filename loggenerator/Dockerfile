FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY csv csv
COPY *.py .

RUN mkdir -p logs && chown -R appuser:appuser /app

USER appuser

CMD ["python", "main.py"]
