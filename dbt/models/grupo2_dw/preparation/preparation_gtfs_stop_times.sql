{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

select
stop_id,
trip_id,
{{ normalize_time('arrival_time') }} AS arrival_time,
{{ normalize_time('departure_time') }} AS departure_time,
{{ is_peak_time('arrival_time') }} AS is_peak,
drop_off_type,
pickup_type,
shape_dist_traveled as distance,
CAST(stop_sequence AS INT64) as stop_sequence,
coalesce(TIME_DIFF(
    {{ normalize_time('arrival_time') }} ,
    LAG({{ normalize_time('arrival_time') }} ) OVER (
      PARTITION BY trip_id
      ORDER BY CAST(stop_sequence AS INT64)
    ),
    MINUTE
  ),0) AS duration_minutes,
timepoint,
line_id,
route_id,
COALESCE(service_id,'N/A') as service_id,
ingestion_date
 from {{ source('carris', 'staging_gtfs_stop_times') }}
