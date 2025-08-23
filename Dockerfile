FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-interaction --no-ansi --no-root

COPY src/ ./src/
COPY .env .env

CMD ["poetry", "run", "uvicorn", "python_fastapi_starter.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
