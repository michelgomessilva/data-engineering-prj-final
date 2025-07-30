{{ config(
    schema='mart_grupo_2',
    materialized='table'
) }}

{% set surrogate_key_columns = ["route_id"] %}

with
    routes as (
        select * from {{ ref("preparation_routes") }}
    ),

   final as (
        select
            {{ dbt_utils.generate_surrogate_key(surrogate_key_columns) }}
            as route_key,
            routes.route_id,
            routes.line_id,
            routes.line_name,
            routes.is_circular,
            routes.path_type,
            routes.ingestion_date
        FROM routes
   )

select * from final
