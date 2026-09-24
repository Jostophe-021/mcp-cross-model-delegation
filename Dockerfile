FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MCP_HOST=127.0.0.1 \
    PORT=8000

WORKDIR /app
RUN pip install --no-cache-dir uv==0.12.9
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY gateway.py server.py ./
COPY providers ./providers
USER 65532:65532
CMD ["/app/.venv/bin/python", "server.py"]
