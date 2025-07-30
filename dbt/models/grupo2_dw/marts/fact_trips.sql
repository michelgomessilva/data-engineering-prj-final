{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

{% set surrogate_key_columns = ["trips.trip_id","stop_id"] %}

with
    stop_times as (
       select trip_id, stop_id, is_peak, stop_sequence from {{ ref("preparation_gtfs_stop_times") }}
    ),

    stop_times_counts as (
        select trip_id, round(sum(cast(distance as float64)),2) as total_trip_distance, sum(duration_minutes) as total_trip_duration
        from {{ ref("preparation_gtfs_stop_times") }}
        group by trip_id
    ),

    trips as (
       select t.trip_id, t.service_id, t.ingestion_date, l.route_key, l.line_name
       from {{ ref("preparation_trips") }} as t
       inner join {{ ref("dim_lines") }} as l on l.route_id = t.route_id
    ),

    calendar_dates as (
       select * from {{ ref("preparation_calendar_dates") }}
       ---fazer inner join com a dim_date tirar sk
    ),

    final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as trip_key,
			trips.trip_id,
			stop_times.stop_id,
			stop_times.stop_sequence,
			trips.route_key as route_id,
            trips.line_name,
			stop_times.is_peak,
			calendar_dates.calendar_date as trip_date,
			total_trip_distance,
			total_trip_duration,
			trips.service_id,
			trips.ingestion_date
        FROM trips
        left join stop_times on trips.trip_id = stop_times.trip_id
        inner join stop_times_counts on trips.trip_id = stop_times_counts.trip_id
        left join calendar_dates on trips.service_id = calendar_dates.service_id
   )

select * from final
