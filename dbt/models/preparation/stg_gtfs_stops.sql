
select
*
 from {{ explode_array(source('carris', 'staging_gtfs_stops'), 'routes', 'route')
