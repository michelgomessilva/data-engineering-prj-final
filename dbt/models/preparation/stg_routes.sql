
select
route_id,
line_id,
line_long_name as line_name,
{{cast_to_boolean('circular') }} as is_circular,
path_type,
ingestion_date
from {{ source('carris', 'staging_gtfs_routes') }}
