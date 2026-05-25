FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

RUN uv run playwright install chromium

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
