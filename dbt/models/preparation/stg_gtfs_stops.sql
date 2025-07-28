
select
*
from {{ source('carris', 'staging_gtfs_stops')}}
where municipality_id is not null
