{{ config(
    schema='preparation_grupo_2',
    materialized='view'
) }}

select
stop_id,
case when
    stop_name_new = 'A DEFINIR' or stop_name_new is null then stop_name
    else stop_name_new
end as name,
case when
    stop_short_name = 'A DEFINIR' OR stop_short_name IS NULL then 'N/A'
    else stop_short_name
end as short_name,
district_id,
municipality_id,
region_id,
district_name,
municipality_name,
region_name,
latitude,
longitude,
case when
    localities IS NULL then 'N/A'
    else localities
end as localities,
operational_status AS status,
tts_stop_name,
{{cast_to_boolean('near_hospital') }} as near_hospital,
{{cast_to_boolean('near_school') }} as near_school,
ingestion_date
from {{ source('carris', 'staging_gtfs_stops') }}
where operational_status = 'ACTIVE'
