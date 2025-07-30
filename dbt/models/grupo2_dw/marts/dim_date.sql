{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}


with
    dates as (
       select * from {{ ref("preparation_date") }}
    ),

   final as (
        select
            sk_date as date_key,
            dates.date_day,
            dates.day,
            dates.month,
            dates.year,
            dates.week_day,
            dates.day_type,
            dates.day_type_description,
            dates.is_holiday,
            dates.type_holiday,
            dates.period_type,
            dates.period_description,
            dates.ingestion_date
        FROM dates
        order by date_day asc
   )

select * from final
