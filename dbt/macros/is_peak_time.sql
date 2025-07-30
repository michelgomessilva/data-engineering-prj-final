{% macro is_peak_time(time_column) %}
    CASE
        -- Morning peak: 07:00:00 to 09:59:59
        WHEN SAFE.PARSE_TIME('%H:%M:%S', {{ time_column }}) BETWEEN PARSE_TIME('%H:%M:%S','07:00:00') AND PARSE_TIME('%H:%M:%S','09:59:59') THEN TRUE

        -- Evening peak: 17:00:00 to 19:59:59
        WHEN SAFE.PARSE_TIME('%H:%M:%S', {{ time_column }}) BETWEEN PARSE_TIME('%H:%M:%S','17:00:00') AND PARSE_TIME('%H:%M:%S','19:59:59') THEN TRUE

        ELSE FALSE
    END
{% endmacro %}
