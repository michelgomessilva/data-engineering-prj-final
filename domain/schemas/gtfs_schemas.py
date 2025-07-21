from pyspark.sql.types import StringType, StructField, StructType

GTFS_SCHEMAS = {
    "agency": StructType(
        [
            StructField("agency_email", StringType(), True),
            StructField("agency_fare_url", StringType(), True),
            StructField("agency_id", StringType(), True),
            StructField("agency_lang", StringType(), True),
            StructField("agency_name", StringType(), True),
            StructField("agency_phone", StringType(), True),
            StructField("agency_timezone", StringType(), True),
            StructField("agency_url", StringType(), True),
        ]
    ),
    "archives": StructType(
        [
            StructField("archive_end_date", StringType(), True),
            StructField("archive_id", StringType(), True),
            StructField("archive_start_date", StringType(), True),
            StructField("operator_id", StringType(), True),
        ]
    ),
    "calendar_dates": StructType(
        [
            StructField("date", StringType(), True),
            StructField("day_type", StringType(), True),
            StructField("exception_type", StringType(), True),
            StructField("holiday", StringType(), True),
            StructField("period", StringType(), True),
            StructField("service_id", StringType(), True),
        ]
    ),
    "dates": StructType(
        [
            StructField("date", StringType(), True),
            StructField("day_type", StringType(), True),
            StructField("holiday", StringType(), True),
            StructField("notes", StringType(), True),
            StructField("period", StringType(), True),
        ]
    ),
    "fare_attributes": StructType(
        [
            StructField("currency_type", StringType(), True),
            StructField("fare_id", StringType(), True),
            StructField("payment_method", StringType(), True),
            StructField("price", StringType(), True),
            StructField("transfers", StringType(), True),
        ]
    ),
    "fare_rules": StructType(
        [
            StructField("fare_id", StringType(), True),
            StructField("route_id", StringType(), True),
        ]
    ),
    "feed_info": StructType(
        [
            StructField("default_lang", StringType(), True),
            StructField("feed_contact_url", StringType(), True),
            StructField("feed_end_date", StringType(), True),
            StructField("feed_lang", StringType(), True),
            StructField("feed_publisher_name", StringType(), True),
            StructField("feed_publisher_url", StringType(), True),
            StructField("feed_start_date", StringType(), True),
            StructField("feed_version", StringType(), True),
        ]
    ),
    "municipalities": StructType(
        [
            StructField("district_id", StringType(), True),
            StructField("district_name", StringType(), True),
            StructField("municipality_id", StringType(), True),
            StructField("municipality_name", StringType(), True),
            StructField("municipality_prefix", StringType(), True),
            StructField("region_id", StringType(), True),
            StructField("region_name", StringType(), True),
        ]
    ),
    "periods": StructType(
        [
            StructField("period_id", StringType(), True),
            StructField("period_name", StringType(), True),
        ]
    ),
    "routes": StructType(
        [
            StructField("agency_id", StringType(), True),
            StructField("circular", StringType(), True),
            StructField("line_id", StringType(), True),
            StructField("line_long_name", StringType(), True),
            StructField("line_short_name", StringType(), True),
            StructField("line_type", StringType(), True),
            StructField("path_type", StringType(), True),
            StructField("route_color", StringType(), True),
            StructField("route_id", StringType(), True),
            StructField("route_long_name", StringType(), True),
            StructField("route_short_name", StringType(), True),
            StructField("route_text_color", StringType(), True),
            StructField("route_type", StringType(), True),
            StructField("school", StringType(), True),
        ]
    ),
    "shapes": StructType(
        [
            StructField("shape_dist_traveled", StringType(), True),
            StructField("shape_id", StringType(), True),
            StructField("shape_pt_lat", StringType(), True),
            StructField("shape_pt_lon", StringType(), True),
            StructField("shape_pt_sequence", StringType(), True),
        ]
    ),
    "stop_times": StructType(
        [
            StructField("arrival_time", StringType(), True),
            StructField("departure_time", StringType(), True),
            StructField("drop_off_type", StringType(), True),
            StructField("pickup_type", StringType(), True),
            StructField("shape_dist_traveled", StringType(), True),
            StructField("stop_id", StringType(), True),
            StructField("stop_sequence", StringType(), True),
            StructField("timepoint", StringType(), True),
            StructField("trip_id", StringType(), True),
        ]
    ),
    "stops": StructType(
        [
            StructField("stop_id", StringType(), True),
            StructField("stop_name", StringType(), True),
            StructField("stop_name_new", StringType(), True),
            StructField("stop_short_name", StringType(), True),
            StructField("stop_lat", StringType(), True),
            StructField("stop_lon", StringType(), True),
            StructField("operational_status", StringType(), True),
            StructField("areas", StringType(), True),
            StructField("region_id", StringType(), True),
            StructField("region_name", StringType(), True),
            StructField("district_id", StringType(), True),
            StructField("district_name", StringType(), True),
            StructField("municipality_id", StringType(), True),
            StructField("municipality_name", StringType(), True),
            StructField("parish_id", StringType(), True),
            StructField("parish_name", StringType(), True),
            StructField("locality", StringType(), True),
            StructField("jurisdiction", StringType(), True),
            StructField("stop_code", StringType(), True),
            StructField("tts_stop_name", StringType(), True),
            StructField("platform_code", StringType(), True),
            StructField("parent_station", StringType(), True),
            StructField("location_type", StringType(), True),
            StructField("stop_url", StringType(), True),
            StructField("has_pole", StringType(), True),
            StructField("has_cover", StringType(), True),
            StructField("has_shelter", StringType(), True),
            StructField("shelter_code", StringType(), True),
            StructField("shelter_maintainer", StringType(), True),
            StructField("has_mupi", StringType(), True),
            StructField("has_bench", StringType(), True),
            StructField("has_trash_bin", StringType(), True),
            StructField("has_lighting", StringType(), True),
            StructField("has_electricity", StringType(), True),
            StructField("docking_bay_type", StringType(), True),
            StructField("last_infrastructure_maintenance", StringType(), True),
            StructField("last_infrastructure_check", StringType(), True),
            StructField("has_flag", StringType(), True),
            StructField("flag_maintainer", StringType(), True),
            StructField("has_pip_static", StringType(), True),
            StructField("has_pip_audio", StringType(), True),
            StructField("pip_audio_code", StringType(), True),
            StructField("has_pip_realtime", StringType(), True),
            StructField("pip_realtime_code", StringType(), True),
            StructField("has_h2oa_signage", StringType(), True),
            StructField("has_schedules", StringType(), True),
            StructField("has_tactile_schedules", StringType(), True),
            StructField("has_network_map", StringType(), True),
            StructField("last_schedules_maintenance", StringType(), True),
            StructField("last_schedules_check", StringType(), True),
            StructField("last_flag_maintenance", StringType(), True),
            StructField("last_flag_check", StringType(), True),
            StructField("has_sidewalk", StringType(), True),
            StructField("sidewalk_type", StringType(), True),
            StructField("has_crossing", StringType(), True),
            StructField("has_flat_access", StringType(), True),
            StructField("has_wide_access", StringType(), True),
            StructField("has_tactile_access", StringType(), True),
            StructField("has_abusive_parking", StringType(), True),
            StructField("wheelchair_boarding", StringType(), True),
            StructField("last_accessibility_maintenance", StringType(), True),
            StructField("last_accessibility_check", StringType(), True),
            StructField("near_health_clinic", StringType(), True),
            StructField("near_hospital", StringType(), True),
            StructField("near_university", StringType(), True),
            StructField("near_school", StringType(), True),
            StructField("near_police_station", StringType(), True),
            StructField("near_fire_station", StringType(), True),
            StructField("near_shopping", StringType(), True),
            StructField("near_historic_building", StringType(), True),
            StructField("near_transit_office", StringType(), True),
            StructField("near_beach", StringType(), True),
            StructField("subway", StringType(), True),
            StructField("light_rail", StringType(), True),
            StructField("train", StringType(), True),
            StructField("boat", StringType(), True),
            StructField("airport", StringType(), True),
            StructField("bike_sharing", StringType(), True),
            StructField("bike_parking", StringType(), True),
            StructField("car_parking", StringType(), True),
        ]
    ),
    "trips": StructType(
        [
            StructField("calendar_desc", StringType(), True),
            StructField("direction_id", StringType(), True),
            StructField("pattern_id", StringType(), True),
            StructField("route_id", StringType(), True),
            StructField("service_id", StringType(), True),
            StructField("shape_id", StringType(), True),
            StructField("trip_headsign", StringType(), True),
            StructField("trip_id", StringType(), True),
        ]
    ),
}
