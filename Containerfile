FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app

COPY uv.lock pyproject.toml .

COPY src ./src

RUN uv sync --frozen && \
    uv pip install -e . && \
    uv build .

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/dist/*.whl .

RUN apt-get update -y && \
    apt-get install -y zstd && \
    rm -rf /var/lib/apt/lists/*

RUN pip install *.whl

CMD ["python", "-m", "mc2sf"]
