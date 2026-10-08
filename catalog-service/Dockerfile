FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app 

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY ../pyproject.toml ../poetry.lock ./
RUN poetry install --no-root --only main

COPY . .

EXPOSE  8000

CMD ["python3", "-m", "uvicorn", "catalog-service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
