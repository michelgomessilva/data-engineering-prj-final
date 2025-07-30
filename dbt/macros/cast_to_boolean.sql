{% macro cast_to_boolean(column_name) %}
    CASE
        WHEN LOWER(TRIM({{ column_name }})) IN ('true', '1', 'yes') THEN TRUE
        WHEN LOWER(TRIM({{ column_name }})) IN ('false', '0', 'no') THEN FALSE
        ELSE NULL
    END
{% endmacro %}
