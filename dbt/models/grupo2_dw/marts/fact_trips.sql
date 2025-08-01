{{ config(
    schema='mart_grupo_2',
    materialized='table',
) }}

{% set surrogate_key_columns = ["trips.trip_id", "stop_times.stop_id", "calendar_dates.sk_date"] %}

with
    stop_times as (
        select
            trip_id,
            stop_id,
            is_peak
        from {{ ref("preparation_gtfs_stop_times") }}
        GROUP BY trip_id, stop_id, is_peak
    ),

    stop_times_agg as (
        select
            trip_id,
            round(sum(cast(distance as float64)), 2) as total_distance,
            sum(duration_minutes) as total_duration
        from {{ ref("preparation_gtfs_stop_times") }}
        group by trip_id
    ),

    off_peak as (
        select
            trip_id,
            CASE
                WHEN COUNT(DISTINCT is_peak) > 1 THEN true
                ELSE MAX(is_peak)
            END AS is_peak_trip
        from {{ ref("preparation_gtfs_stop_times") }}
        group by trip_id
    ),

    trips as (
        select DISTINCT
            t.trip_id,
            t.service_id,
            t.pattern_id,
            t.route_id as sk_line,
            l.line_name as line_id
        from {{ ref("preparation_trips") }} as t
        inner join {{ ref("dim_lines") }} as l
        on l.route_id = t.route_id
    ),

    calendar_dates as (
       select distinct service_id, sk_date
       from {{ ref("preparation_calendar_dates") }} as cd
       inner join {{ ref("dim_date") }}  as dd
       ON cd.calendar_date = dd.date_day
    ),

    final as (
        select DISTINCT
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }} as trip_key,
            trips.trip_id,
            stop_times.stop_id as sk_stop,
            trips.sk_line,
            trips.line_id,
            calendar_dates.sk_date as trip_date,
            off_peak.is_peak_trip,
            stop_times_agg.total_duration as trip_duration,
            stop_times_agg.total_distance as distance,
            trips.pattern_id,
            trips.service_id,
            current_timestamp() as created_at,
            current_timestamp() as last_updated_at,
        from trips
        INNER join stop_times on trips.trip_id = stop_times.trip_id
        INNER join calendar_dates on trips.service_id = calendar_dates.service_id
        inner join stop_times_agg on trips.trip_id = stop_times_agg.trip_id
        inner join off_peak on trips.trip_id = off_peak.trip_id
    )

select * from final
