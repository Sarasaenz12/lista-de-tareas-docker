FROM python:3.12-slim

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copiar dependencias primero (caché de Docker)
COPY pyproject.toml .

# Instalar dependencias (incluyendo dev para pruebas)
RUN uv pip install --system -e ".[dev]"

# Copiar el resto del código
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]