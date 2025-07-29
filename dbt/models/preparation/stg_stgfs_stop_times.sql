
select
stop_id,
trip_id,
PARSE_TIME('%H:%M:%S',arrival_time) AS arrival_time,
PARSE_TIME('%H:%M:%S',departure_time) AS departure_time,
drop_off_type,
pickup_type,
shape_dist_traveled,
stop_sequence,
timepoint,
line_id,
route_id,
COALESCE(service_id,'N/A'),
ingestion_date
 from {{ (source('carris', 'staging_gtfs_stops') }}
