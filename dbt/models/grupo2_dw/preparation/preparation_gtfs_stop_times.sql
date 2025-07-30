{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

select
stop_id,
trip_id,
SAFE.PARSE_TIME('%H:%M:%S',arrival_time) AS arrival_time,
SAFE.PARSE_TIME('%H:%M:%S',departure_time) AS departure_time,
{{ is_peak_time('arrival_time') }} AS is_peak,
drop_off_type,
pickup_type,
shape_dist_traveled as distance,
stop_sequence,
timepoint,
line_id,
route_id,
COALESCE(service_id,'N/A') as service_id,
ingestion_date
 from {{ source('carris', 'staging_gtfs_stop_times') }}
