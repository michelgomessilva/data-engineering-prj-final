{% set surrogate_key_columns = ["municipality_id"] %}

with
    municipalities as (
        select * from {{ ref("stg_municipalities") }}
    ),

   final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as municipality_key,
            municipalities.municipality_id,
            municipalities.municipality_name,
            municipalities.district_id,
            municipalities.district_name,
            municipalities.region_id,
            municipalities.region_name,
            municipalities.municipality_prefix,
            municipalities.ingestion_date
        FROM municipalities
   )

select * from final
