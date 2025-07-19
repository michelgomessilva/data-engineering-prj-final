# -------------------
# Stage 1: Builder
# -------------------
FROM python:3.10-slim AS builder

# Instala Java e dependências do sistema
RUN apt-get update && \
    apt-get install -y default-jdk curl build-essential && \
    apt-get clean

# Detecta e exporta JAVA_HOME dinamicamente (Java 17, por ex.)
RUN JAVA_PATH=$(readlink -f $(which java)) && \
    JAVA_HOME=$(dirname $(dirname "$JAVA_PATH")) && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment && \
    echo "PATH=$JAVA_HOME/bin:$PATH" >> /etc/environment

# Instala Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $HOME/.local/bin/poetry /usr/local/bin/poetry

# Define diretório de trabalho da aplicação
WORKDIR /app

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# -------------------
# Stage 2: Runtime
# -------------------
FROM python:3.10-slim AS runtime

# Instala Java no container final
RUN apt-get update && \
    apt-get install -y default-jdk && \
    # Detecta e salva o JAVA_HOME dinamicamente
    JAVA_PATH=$(readlink -f $(which java)) && \
    JAVA_HOME=$(dirname $(dirname "$JAVA_PATH")) && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment && \
    echo "PATH=$JAVA_HOME/bin:$PATH" >> /etc/environment && \
    apt-get clean

# Exporta JAVA_HOME em tempo de execução (reforço para Spark)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Define diretório de trabalho
WORKDIR /app

# Copia as dependências instaladas no builder
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

# Copia o restante do projeto
COPY . .

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Ponto de entrada da aplicação
ENTRYPOINT ["python", "-m", "app.entrypoint"]
