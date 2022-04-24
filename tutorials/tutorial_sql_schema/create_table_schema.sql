CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    {table_column_name}
)
COMMENT '{table_description}'
PARTITIONED BY ({partitioned_column} STRING COMMENT '{partitioned_column_comment}')
STORED AS PARQUET
LOCATION '{s3_bucket}'
tblproperties ("parquet.compression"="SNAPPY");
