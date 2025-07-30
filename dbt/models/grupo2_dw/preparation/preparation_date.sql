{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

with
preparation_date as (
select
SAFE.PARSE_DATE('%Y%m%d', date) as date_day,
day_type,
holiday,
notes,
period,
ingestion_date
from {{ source('carris', 'staging_gtfs_dates') }}
),

preparation_period as (
select
*
from {{ source('carris', 'staging_gtfs_periods') }}
)

select
date_day,
EXTRACT(DAY FROM date_day) AS day,
EXTRACT(MONTH FROM date_day) AS month,
EXTRACT(YEAR FROM date_day) AS year,
EXTRACT(DAYOFWEEK FROM date_day) AS week_day,
day_type,
CASE WHEN day_type = '1' THEN 'Dia útil'
WHEN day_type = '2' THEN 'Sábado'
WHEN day_type = '3' THEN 'Domingo/Feriado'
END as day_type_description,
{{cast_to_boolean('holiday') }} as is_holiday,
coalesce(notes,'N/A') as type_holiday,
preparation_period.period_id as period_type,
preparation_period.period_name as period_description,
preparation_date.ingestion_date
from preparation_date
INNER JOIN preparation_period on preparation_date.period = preparation_period.period_id
