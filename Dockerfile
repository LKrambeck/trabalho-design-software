FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema (opcional, útil para build mais estável)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copiar pyproject para instalar deps
COPY pyproject.toml /app/

# Copiar código
COPY src /app/src

# Instalar dependências
RUN pip install --no-cache-dir uvicorn && \
    pip install --no-cache-dir .

# Expor porta
EXPOSE 8000

# Comando
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]