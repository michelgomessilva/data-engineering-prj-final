{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

with dates as (
    select * from {{ ref("preparation_date") }}
),

final as (
    select
        -- Chave surrogate no formato aaaammdd (ex: 20250731)
        cast(format_date('%Y%m%d', date_day) as int64) as sk_date,

        -- Campos principais
        date_day,
        day,
        month,
        year,
        cast(week_day as int64) as week_day,
        cast(day_type as int64) as day_type,
        day_type_description,
        is_holiday,
        type_holiday,
        period_type,
        period_description,
        ingestion_date
    from dates
)

select * from final
