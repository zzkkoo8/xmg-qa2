FROM node:24.17.0-bookworm-slim AS web-build
WORKDIR /build/web
RUN corepack enable
COPY web/package.json web/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY web/ ./
RUN pnpm build

FROM ghcr.io/astral-sh/uv:0.12.5 AS uv

FROM python:3.12.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app
COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
RUN uv sync --frozen --no-dev
COPY --from=web-build /build/web/dist ./web/dist
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-c", "import time, xmg_qa2; time.sleep(3600)"]
