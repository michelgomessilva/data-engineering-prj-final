{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

select
trip_id,
route_id,
pattern_id,
shape_id,
service_id,
direction_id,
trip_headsign as destination,
coalesce(calendar_desc,'N/A') as occasional_trip,
ingestion_date
from {{ source('carris', 'staging_gtfs_trips') }}
