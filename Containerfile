FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY uv.lock pyproject.toml .

COPY src ./src

RUN uv sync --frozen && \
    uv pip install -e .

ENTRYPOINT ["uv", "run", "mc2sf"]
