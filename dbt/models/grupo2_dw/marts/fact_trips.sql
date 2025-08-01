{{ config(
    schema='mart_grupo_2',
    materialized='table',
) }}

{% set surrogate_key_columns = ["trips.trip_id", "stop_times.stop_id"] %}

with
    stop_times as (
        select
            trip_id,
            stop_id,
--            stop_sequence,
            is_peak,
            arrival_time,
            departure_time,
            distance,
            duration_minutes
        from {{ ref("preparation_gtfs_stop_times") }}
    ),

    stop_times_agg as (
        select
            trip_id,
            round(sum(cast(distance as float64)), 2) as total_distance,
            sum(duration_minutes) as total_duration
        from {{ ref("preparation_gtfs_stop_times") }}
        group by trip_id
    ),

    trips as (
        select
            t.trip_id,
            t.service_id,
            t.pattern_id,
            t.ingestion_date,
            l.route_key as sk_line,
            l.line_name as line_id
        from {{ ref("preparation_trips") }} as t
        inner join {{ ref("dim_lines") }} as l
            on l.route_id = t.route_id
    ),

    calendar_dates as (
        select service_id, calendar_date
        from {{ ref("preparation_calendar_dates") }}
    ),

    dim_date as (
        select sk_date, date_day
        from {{ ref("dim_date") }}
    ),

    final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }} as trip_key,
            stop_times.stop_id as sk_stop,
            trips.sk_line,
            trips.line_id,
            dim_date.sk_date as trip_date,
            stop_times.departure_time,
            stop_times.arrival_time,
            stop_times.is_peak as is_peak_time,
            stop_times_agg.total_duration as trip_duration,
            stop_times_agg.total_distance as distance,
            trips.pattern_id,
            trips.service_id,
            current_timestamp() as created_at,
            current_timestamp() as last_updated_at,
        from trips
        left join stop_times on trips.trip_id = stop_times.trip_id
        left join calendar_dates on trips.service_id = calendar_dates.service_id
        left join dim_date on calendar_dates.calendar_date = dim_date.date_day
        inner join stop_times_agg on trips.trip_id = stop_times_agg.trip_id
    )

select * from final
