{% macro normalize_time(column_name) %}
--SAFE.PARSE_TIME(
--  '%H:%M',
--  FORMAT(
--    "%02d:%02d",
--    MOD(CAST(SPLIT({{ column_name }}, ":")[OFFSET(0)] AS INT64), 24),
--    CAST(SPLIT({{ column_name }}, ":")[OFFSET(1)] AS INT64)
--  )
--)
TIME(
  MOD(CAST(SPLIT({{ column_name }}, ":")[OFFSET(0)] AS INT64), 24),
  CAST(SPLIT({{ column_name }}, ":")[OFFSET(1)] AS INT64),
  0
)
{% endmacro %}
