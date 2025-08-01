# Data Engineering - Projeto Final

Este projeto segue os princípios da **Clean Architecture**, adaptados para **pipelines de engenharia de dados** utilizando Python. O objetivo é garantir uma organização modular, com separação clara de responsabilidades, testabilidade e facilidade de manutenção e evolução da solução ao longo do tempo.

---

## 🧱 Estrutura de Pastas

```bash
project_name/
├── README.md                       # Documentação do projeto
├── pyproject.toml                  # Gerenciador de dependências (Poetry)
├── requirements.txt                # Dependências (caso não use Poetry)
├── .env                            # Variáveis de ambiente sensíveis
├── .gitignore                      # Arquivos ignorados pelo Git

├── app/                            # Camada de apresentação (entrypoint)
│   └── main.py                     # Ponto principal de execução dos pipelines

├── domain/                         # Regras de negócio (domínio)
│   ├── models/                     # Entidades ou DTOs (ex: Vehicle, Route)
│   └── services/                   # Abstrações de serviços de negócio

├── application/                    # Casos de uso (application services)
│   ├── use_cases/                  # Orquestração de operações (ex: ingest_vehicles)
│   └── pipelines/                  # Pipelines por caso de uso (ex: daily_pipeline)

├── infrastructure/                # Implementações concretas (APIs, Spark, Repos)
│   ├── api/                        # Acesso a fontes externas (ex: APIs REST)
│   ├── spark/                      # Inicialização da sessão Spark e helpers
│   ├── storage/                    # Leitura/gravação (Parquet, CSV, etc.)
│   └── repositories/              # Persistência com lógica concreta

├── configs/                        # Configurações globais do projeto
│   └── settings.py

├── tests/                          # Testes automatizados
│   ├── unit/                       # Testes unitários
│   ├── integration/                # Testes de ponta a ponta
│   └── conftest.py                 # Fixtures globais

└── dags/                           # (opcional) DAGs com Apache Airflow
    └── data_ingestion_dag.py
```

---

## 💡 Motivação da Arquitetura

A estrutura é inspirada em *Clean Architecture* de Robert C. Martin (Uncle Bob), com adaptações para projetos de engenharia de dados. Os principais benefícios incluem:

- **Separação de interesses:** domínio desacoplado da infraestrutura.
- **Testabilidade:** cada camada pode ser testada isoladamente.
- **Reusabilidade:** pipelines reutilizam casos de uso e serviços.
- **Flexibilidade:** fácil trocar implementações (ex: Parquet ↔ Delta Lake).
- **Escalabilidade:** o projeto cresce de forma modular e organizada.

---

## 🔄 Fluxo de Execução

1. O arquivo `main.py` inicia a execução da pipeline.
2. A pipeline utiliza **casos de uso** definidos em `application/use_cases/`.
3. Esses casos acessam **serviços e modelos** definidos na `domain/`.
4. A infraestrutura provê os meios técnicos para extrair, transformar e carregar os dados:

   - APIs externas (ex: Carris Metropolitana)
   - Armazenamento em arquivos (ex: Parquet)
   - Spark para processamento distribuído

---

## 🧪 Testes

Os testes estão organizados da seguinte forma:

- `tests/unit`: validações de lógica isolada (funções, transformações, validações).
- `tests/integration`: verificação de integração entre partes do sistema (ex: API + Spark + persistência).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **PySpark**
- **Poetry**
- **.env** para configurações de ambiente
- **Apache Airflow**
- **pytest** para testes automatizados

---

## 📦 Como Executar

```bash
# Instalar dependências com Poetry
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\bootstrap.ps1

# Verificar se já tem o ficheiro das credencials locais
cp "C:/Users/miche/AppData/Roaming/gcloud/application_default_credentials.json" ./gcp-key.json

# Para criar a imagem docker
docker build -t grupo-2-pipeline-app .

# Executar pipeline de ingestão para um único caso de uso
docker run --rm `
  -v "${PWD}/gcp-key.json:/app/gcp-key.json" `
  grupo-2-pipeline-app python -m app.main --use-case ingest_vehicles

# Executar pipeline com todos os casos de uso de ingestão
docker run --rm `
  -v "${PWD}/gcp-key.json:/app/gcp-key.json" `
  grupo-2-pipeline-app python -m app.main --use-case all

# Executar pipeline de cleansing para um único caso de uso
docker run --rm `
  -v "${PWD}/gcp-key.json:/app/gcp-key.json" `
  grupo-2-pipeline-app python -m app.main --use-case cleanse_gtfs_stop_times

# Executar dbt através do docker
docker run --rm `
  -v "${PWD}/gcp-key.json:/app/gcp-key.json" `
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json `
  --entrypoint dbt `
  grupo-2-pipeline-app run --project-dir /app/dbt

# Executar dbt através do docker com um model específico
docker run --rm `
  -v "${PWD}/gcp-key.json:/app/gcp-key.json" `
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json `
  --entrypoint dbt `
  grupo-2-pipeline-app run --project-dir /app/dbt --select my_model

```

---

## 📂 Exemplo de Expansão

Para adicionar uma nova fonte de dados:

1. Crie um repositório ou cliente em `infrastructure/`.
2. Defina a interface correspondente em `domain/services/`.
3. Implemente um novo caso de uso em `application/use_cases/`.

---

## 📘 Referências

- [Clean Architecture - Robert C. Martin](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
