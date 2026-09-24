FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_HOST=127.0.0.1 \
    PORT=8000

WORKDIR /app
RUN pip install --no-cache-dir uv==0.12.9
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --extra all --no-install-project
COPY *.py ./
COPY providers ./providers
COPY benchmarks ./benchmarks
RUN uv sync --frozen --no-dev --extra all --offline
USER 65532:65532
CMD ["/app/.venv/bin/crossmodel", "serve"]
