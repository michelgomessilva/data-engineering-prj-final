{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

with
preparation_calendar_date as (
select
SAFE.PARSE_DATE('%Y%m%d', date) as calendar_date,
day_type,
CASE WHEN day_type = '1' THEN 'Dia útil'
WHEN day_type = '2' THEN 'Sábado'
WHEN day_type = '3' THEN 'Domingo/Feriado'
END as day_type_description,
{{cast_to_boolean('holiday') }} as is_holiday,
period,
service_id,
ingestion_date
from {{ source('carris', 'staging_gtfs_calendar_dates') }}
),

preparation_period as (
select
*
from {{ source('carris', 'staging_gtfs_periods') }}
)

select
calendar_date,
day_type,
day_type_description,
is_holiday,
preparation_period.period_id as period_type,
preparation_period.period_name as period_description,
service_id,
preparation_calendar_date.ingestion_date
from preparation_calendar_date
INNER JOIN preparation_period on preparation_calendar_date.period = preparation_period.period_id
