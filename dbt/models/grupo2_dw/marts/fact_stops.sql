{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

{% set surrogate_key_columns = ["stop_id","route_id","calendar_date"] %}

with
    stops as (
       select distinct stop_key as sk_stop, stop_id, near_school, m.municipality_key as sk_municipalities, m.region_name, m.municipality_name
       from {{ ref("dim_stops") }} as s
       inner join {{ ref("dim_municipalities") }} as m on m.municipality_id = s.municipality_id
    ),

    stop_times as (
       select distinct stops.*, trip_id from stops
       INNER join {{ ref("preparation_gtfs_stop_times") }} st on stops.stop_id = st.stop_id
    ),

    stop_trips as (
       select distinct st.*, service_id, route_id from stop_times st
       INNER join {{ ref("preparation_trips") }} t on st.trip_id = t.trip_id
    ),

    stop_service_line as (
       select distinct st.*, l.route_key as sk_line, l.line_id
       from stop_trips as st
       inner join {{ ref("dim_lines") }} as l on l.route_id = st.route_id
    ),

    stop_line_calendar_date as (
       select distinct ssl.*, cd.calendar_date
       from stop_service_line ssl
       inner join {{ ref("preparation_calendar_dates") }} as cd on ssl.service_id = cd.service_id
    ),

    stop_line_calendar_date_aggr as (
       select distinct stop_id, line_id, calendar_date, count(1) as total_line_stops
       from stop_line_calendar_date
       group by stop_id, line_id, calendar_date
   ),

    stop_line_date_aggr as (
       select distinct slcd.*, sk_date, day_type_description AS day_type, period_description as period, total_line_stops
       from stop_line_calendar_date slcd
       inner join stop_line_calendar_date_aggr aggr on slcd.stop_id = aggr.stop_id
       and slcd.line_id = aggr.line_id and aggr.calendar_date = slcd.calendar_date
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
            day_type,
			period,
			near_school as is_near_school,
			municipality_name,
			region_name,
			total_line_stops,
            -- Controle incremental
            current_timestamp() as created_at,
            current_timestamp() as last_updated_at
        FROM stop_line_date_aggr
   )

select * from final
