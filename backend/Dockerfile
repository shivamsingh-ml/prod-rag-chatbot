FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy config and install dependencies
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy source code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    