{% macro explode_array(table, array_column, alias='exploded') %}
    (
        SELECT
            * EXCEPT({{ array_column }}),
            {{ array_column }}_element AS {{ alias }}
        FROM {{ table }},
        UNNEST({{ array_column }}) AS {{ array_column }}_element
    )
{% endmacro %}
