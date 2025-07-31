{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

{% set surrogate_key_columns = ["stop_id","line_id","calendar_date"] %}

with
    stops as (
       select stop_key as sk_stop, stop_id, near_school, m.municipality_key as sk_municipalities, m.region_name
       from {{ ref("dim_stops") }} as s
       inner join {{ ref("dim_municipalities") }} as m on m.municipality_id = s.municipality_id
    ),

    stop_service as (
       select stops.*, service_id, route_id, ingestion_date from stops
       left join {{ ref("preparation_gtfs_stop_times") }} st on stops.stop_id = st.stop_id
    ),

    stop_service_line as (
       select ss.*, l.route_key as sk_line, l.line_id
       from stop_service as ss
       inner join {{ ref("dim_lines") }} as l on l.route_id = ss.route_id
    ),

    stop_line_calendar_date as (
       select ssl.*, cd.calendar_date
       from stop_service_line ssl
       left join {{ ref("preparation_calendar_dates") }} as cd on ssl.service_id = cd.service_id
    ),

    stop_line_date as (
       select slcd.*, date_key as sk_date, day_type_description, period_description
       from stop_line_calendar_date slcd
       left join {{ ref("dim_date") }} as dd on dd.date_day = slcd.calendar_date
    ),

    final as (
        select
            distinct
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as f_stop_key,
			sk_line,
			sk_stop,
			sk_date,
			sk_municipalities,
            day_type_description,
			period_description,
			near_school as is_near_school,
			region_name,
            -- Controle incremental
            current_timestamp() as created_at,
            current_timestamp() as last_updated_at
        FROM stop_line_date
   )

select * from final
