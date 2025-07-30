{% set surrogate_key_columns = ["date_day"] %}

with
    dates as (
       select * from {{ ref("stg_date") }}
    ),

   final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as date_key,
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
