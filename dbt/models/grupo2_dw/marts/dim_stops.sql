{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

{% set surrogate_key_columns = ["stop_id"] %}

with
    stops as (
       select * from {{ ref("preparation_gtfs_stops") }}
    ),

   final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as stop_key,
			stops.stop_id,
			stops.name,
			stops.short_name,
			stops.district_id,
			stops.municipality_id,
			stops.region_id,
			stops.district_name,
			stops.municipality_name,
			stops.region_name,
			stops.latitude,
			stops.longitude,
			stops.localities,
			stops.status,
			stops.tts_stop_name,
			stops.near_hospital,
			stops.near_school,
			stops.ingestion_date
        FROM stops
   )

select * from final
