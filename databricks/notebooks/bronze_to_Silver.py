# Databricks notebook source
from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

# COMMAND ----------

df = spark.read.format("parquet")\
    .load("abfss://bronze@adlssmart1211.dfs.core.windows.net/SalesLT/Address/Address.parquet")


# COMMAND ----------

df = df.withColumn("ModifiedDate", date_format(from_utc_timestamp(
    df["ModifiedDate"].cast(TimestampType()), 'UTC'), 'yyyy-MM-dd'))


# COMMAND ----------

table_name = []
for i in dbutils.fs.ls("abfss://bronze@adlssmart1211.dfs.core.windows.net/SalesLT"):
    table_name.append(i.name.split("/")[0])


# COMMAND ----------

for table in table_name:
    path = "abfss://bronze@adlssmart1211.dfs.core.windows.net/SalesLT/" + \
        table + "/" + table + ".parquet"
    df = spark.read.format("parquet").load(path)
    columns = df.columns

    for col in columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, date_format(from_utc_timestamp(
                df[col].cast(TimestampType()), 'UTC'), 'yyyy-MM-dd'))
    outpath = "abfss://silver@adlssmart1211.dfs.core.windows.net/SalesLT/" + table + '/'
    df.write.mode("overwrite").format("delta").save(outpath)

# COMMAND ----------
