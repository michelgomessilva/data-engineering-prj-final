
# 📊 Relatório Técnico: Projeto final Curso Data Engineering

## 1. Introdução

Este projeto final de Data Engineering
tem como objetivo construir uma pipeline robusta e escalável para ingestão,
transformação e carregamento de dados, simulando um processo de batching.
Os dados ingeridos provêm da API da Carris, são carregados no BigQuery através do PySpark e,
posteriormente, são transformados com recurso ao dbt
O propósito principal é garantir a qualidade, integridade e acessibilidade dos dados para suportar análises
e tomadas de decisão informadas.
Todo este processo ELT será orquestrado em diferentes etapas com recurso ao Apache Airflow.

## 2. Arquitetura da Solução

A arquitetura adotada neste projeto segue os princípios de processamento batch e ELT,
garantindo escalabilidade, modularidade e resiliência.

**Componentes principais:**
- **Fontes de dados**: *API da Carris*
- **Ingestão**: *PySpark*
- **Processamento e transformação**: *(PySpark e dbt)*
- **Armazenamento**: *Google Cloud Storage Bucket (Raw Layer) e BigQuery (Staging Layer e Mart Layer)*
- **Orquestração**: *Apache Airflow*

	- Cada pipeline é representado por um DAG.
	- DAGs controlam:
	  1. Extração de dados e gravação no GCS
	  2. Carregamento para BigQuery (staging)
	  3. Transformações e criação de tabelas mart
	- Reprocessamento por `execution_date`, logging, alertas e monitorização pela UI.

- **Destino final (consumo)**: *BigQuery - Marts Layer* -- Apagar??

> 🔁 Sugestão: incluir um diagrama de arquitetura aqui (ex: em formato imagem ou PlantUML - imagens/arquitectura.png)

## 3. Modelo de Dados Final

O modelo de dados foi desenhado para suportar análises de negócio com foco em performance e clareza. Utilizámos um esquema em estrela composto por:

- **Tabelas Fato**: *(ex: fact_sales, fact_orders)*
- **Tabelas Dimensão**: *(ex: dim_customers, dim_products, dim_date)*

**Exemplo de estrutura da tabela `fact_sales`:**
| Campo           | Tipo     | Descrição                    |
|----------------|----------|------------------------------|
| sale_id         | INT      | Identificador único da venda |
| customer_id     | INT      | FK para `dim_customers`      |
| product_id      | INT      | FK para `dim_products`       |
| sale_date       | DATE     | Data da venda                |
| amount          | FLOAT    | Valor da venda               |

> 📐 Sugestão: adicionar aqui um diagrama ER ou modelo estrela.

## 4. Pipeline de Dados: Extract Load and Transform (ETL/ELT)

### 4.1 Data Ingestion

- **Fontes**: *API da Carris - Fornece informação detalhada à cerca de linhas, rotas, paragens, horários, entre outros*
- **Frequência**: *diária, em batch*
- **Ferramentas utilizadas**: *Spark, GCS*

#### 4.1.1 Endpoints utilizados

Tendo em conta a informação a analisar relativa a Stops e Trips, decidimos carregar informações dos seguintes endpoints:

##### 4.1.1.1 gtfs

##### 4.1.1.2 vehicles

	- Devolve informação sobre todos os veículos operados pela carris, nomeadamente a última localização conhecida

	Exemplo resposta:
	{
        id: "41|1153",
        lat: 38.740165,
        lon: -9.268897,
        speed: 0,
        heading: 68.0999984741211,
        trip_id: "1724_0_2_2030_2059_0_7",
        pattern_id: "1724_0_2"
        timestamp: 1693948520000,
    }

##### 4.1.1.3 municipalities
	- Devolve informação sobre os municípios na zona metropolitana de Lisboa, bem como a área adjacente onde a Carris disponibiliza os seus serviços

	Exemplo resposta:
    {
        id: "1502",
        name: "Alcochete",
        prefix: "01",
        district_id: "15",
        district_name: "Setúbal",
        region_id: "PT170",
        region_name: "AML",
    }


##### 4.1.1.4 stops

##### 4.1.1.5 lines

##### 4.1.1.6 routes

##### 4.1.1.7 datasets/facilities

### 4.2 Data Cleansing

- Remoção de duplicados e nulos
- Padronização de campos (datas, texto, códigos)
- Validação de chaves estrangeiras

### 4.3 Data Modelling

- Agregações (ex: vendas por dia, cliente, região)
- Criação de campos derivados (ex: ano-mês, flags)
- Junções entre entidades
- Normalização e desnormalização quando necessário

## 5. Decisões Técnicas e Justificações

**Principais decisões tomadas:**

- **Estrutura em camadas bronze/silver/gold**: facilita rastreabilidade e reprocessamento.
- **Uso de PySpark** para transformar dados em larga escala devido à sua performance distribuída.
- **Armazenamento em formato Parquet** pelas vantagens de compressão e leitura otimizada.
- **Particionamento por data** para melhorar a performance de leitura em queries analíticas.
- **Orquestração com Airflow** para maior controlo e monitorização da pipeline.

> 🧠 Cada decisão foi tomada considerando um equilíbrio entre performance, custo, simplicidade e manutenção futura através do recurso a parametrizações e modulação do código.

## 6. Considerações Finais

O projeto atingiu os objetivos iniciais de criação de uma pipeline confiável e eficiente. O modelo de dados permite análise rápida e precisa. Como próximos passos, sugere-se:

- Implementação de testes automatizados de dados
- Monitorização ativa de qualidade e latência
- Expansão para novas fontes e integração com ferramentas de BI


\* _Adaptar os termos e exemplos entre parêntesis ao teu caso específico._
