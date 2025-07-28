
select
*
from {{ source('carris', 'staging_municipalities')}}
where municipality_id is not null
