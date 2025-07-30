{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

select
municipality_id,
municipality_name,
district_id,
district_name,
region_id,
region_name,
prefix as municipality_prefix,
ingestion_date
from {{ source('carris', 'staging_municipalities')}}
where municipality_id is not null
