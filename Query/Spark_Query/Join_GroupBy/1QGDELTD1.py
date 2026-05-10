from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("HiveQL_Query_<Table_Name>") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("use <credential>")

start_time = time.time()

result_df = spark.sql("""
select a.Actor1Code, a.Actor1Name, 
    count (distinct a.GLOBALEVENTID) as EventCount,

    sum (case when a.GoldsteinScale < -5 then 1 else 0 end) as HigherConflict,
    sum (case when a.GoldsteinScale >= -5 and a.GoldsteinScale < 0 then 1 else 0 end) as LesserConflict,
    sum (case when a.GoldsteinScale = 0 then 1 else 0 end) as Neutral,
    sum (case when a.GoldsteinScale > 0 and a.GoldsteinScale <= 5 then 1 else 0 end) as LesserCooperation,
    sum (case when a.GoldsteinScale > 5 then 1 else 0 end) as HigherCooperation,

    round(
        (sum (case when a.GoldsteinScale > 0 and a.GoldsteinScale <= 5 then 1 else 0 end)
        + sum (case when a.GoldsteinScale > 5 then 1 else 0 end)) * 1.0 /
        (sum (case when a.GoldsteinScale < -5 then 1 else 0 end)
        + sum (case when a.GoldsteinScale >= -5 and a.GoldsteinScale < 0 then 1 else 0 end) + 1), 2
    ) as PolarityRatio

FROM (
    SELECT * FROM <Table_Name> 
    WHERE pmod(hash(Actor1Code), 128) < 64 ) a

JOIN <Table_Name> b
    ON a.GLOBALEVENTID = b.GLOBALEVENTID

where a.Actor1Code is not NULL
  and b.Actor1Code is not NULL
  and trim (a.Actor1Name) != ''

group by a.Actor1Code, a.Actor1Name
order by EventCount 
desc limit 10
""")

result_df.show(truncate=False)

end_time = time.time()
print("Query execution time:", round(end_time - start_time, 2), "seconds")

spark.stop()
