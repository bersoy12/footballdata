## Get all table names

````sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
```


SELECT
    column_name,
    data_type
FROM
    information_schema.columns
WHERE
    table_name = 'match'
ORDER BY
    ordinal_position;



SELECT DISTINCT season_id FROM match;

