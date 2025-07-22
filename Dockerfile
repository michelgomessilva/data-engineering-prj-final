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
COPY poetry.lock pyproject.toml ./

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# -------------------
# Stage 2: Runtime
# -------------------
FROM python:3.10-slim AS runtime

# Instala Java no container final
RUN apt-get update && \
    apt-get install -y default-jdk curl && \
    JAVA_PATH=$(readlink -f $(which java)) && \
    JAVA_HOME=$(dirname $(dirname "$JAVA_PATH")) && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment && \
    echo "PATH=$JAVA_HOME/bin:$PATH" >> /etc/environment && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Baixa e adiciona o JAR do conector do GCS
RUN set -eux; \
    mkdir -p /opt/spark/jars; \
    curl -L -o /opt/spark/jars/gcs-connector-hadoop3-2.2.20-shaded.jar \
      https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.20/gcs-connector-hadoop3-2.2.20-shaded.jar; \
    # remove conectores/guava que vêm com o PySpark
    rm -f /usr/local/lib/python3.10/site-packages/pyspark/jars/gcs-connector-*.jar; \
    rm -f /usr/local/lib/python3.10/site-packages/pyspark/jars/guava-*.jar

WORKDIR /app

# Copia dependências e código
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY . .

# Copia credencial se existir
ARG GCP_KEY_JSON_PATH=gcp-key.json
COPY ${GCP_KEY_JSON_PATH} /app/gcp-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

ENTRYPOINT ["python", "-m", "app.entrypoint"]
