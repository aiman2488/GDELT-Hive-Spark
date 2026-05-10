from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("HiveQL_Query_<Table_Name>") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("use <credential>")

start_time = time.time()

result_df = spark.sql("""
SELECT 
    SUM(LENGTH(full_row)) AS total_character_count,
    SUM(SIZE(SPLIT(TRIM(full_row), ' '))) AS total_word_count,
    SUM(LENGTH(REGEXP_REPLACE(full_row, '[^0-9]', ''))) AS total_numerical_count

FROM (
    SELECT CONCAT_WS(' ', 
Actor1Code,
Actor1Name, 
Actor1CountryCode,
Actor1KnownGroupCode,
Actor1EthnicCode,
Actor1Religion1Code, 
Actor1Religion2Code, 
Actor1Type1Code, 
Actor1Type2Code, 
Actor1Type3Code, 
Actor2Code, 
Actor2Name, 
Actor2CountryCode, 
Actor2KnownGroupCode, 
Actor2EthnicCode,
Actor2Religion1Code, 
Actor2Religion2Code,
Actor2Type1Code, 
Actor2Type2Code, 
Actor2Type3Code, 
EventCode, 
EventBaseCode, 
EventRootCode, 
Actor1Geo_FullName, 
Actor1Geo_CountryCode, 
Actor1Geo_ADM1Code, 
Actor2Geo_FullName, 
Actor2Geo_CountryCode, 
Actor2Geo_ADM1Code, 
ActionGeo_FullName, 
ActionGeo_CountryCode, 
ActionGeo_ADM1Code, 
SOURCEURL
    ) AS full_row 
    FROM <Table_Name>
    WHERE pmod(hash(Actor1Code), 128) < 64
    AND DATEADDED = 20260215
)
""")

result_df.show(truncate=False)

end_time = time.time()
print("Query execution time:", round(end_time - start_time, 2), "seconds")

spark.stop()

