# Databricks notebook source
from pyspark.sql.functions import col

# COMMAND ----------

df = spark.read.format("delta").load("abfss://silver@adlssmart1211.dfs.core.windows.net/SalesLT/Address")


# COMMAND ----------

def rename_columns_to_snake_case(df):
    """
    Convert column names from PascalCase or camelCase to snake_case in a PySpark DataFrame.

    Args:
        df (DataFrame): The input DataFrame with columns to be renamed.

    Returns:
        DataFrame: A new DataFrame with column names converted to snake_case.
    """
    
    column_names = df.columns

    rename_map = {}

    for old_col_name in column_names:
        
        new_col_name = "".join([
            "_" + char.lower() if (
                char.isupper()              
                and idx > 0                
                and not old_col_name[idx - 1].isupper()  
            ) else char.lower()
            for idx, char in enumerate(old_col_name)
        ]).lstrip("_")

        if new_col_name in rename_map.values():
            raise ValueError(f"Duplicate column name found after renaming: '{new_col_name}'")

        rename_map[old_col_name] = new_col_name

    for old_col_name, new_col_name in rename_map.items():
        df = df.withColumnRenamed(old_col_name, new_col_name)

    return df


# COMMAND ----------

table_name = []
for i in dbutils.fs.ls("abfss://silver@adlssmart1211.dfs.core.windows.net/SalesLT"):
    table_name.append(i.name.split("/")[0])
print(table_name)

# COMMAND ----------

for name in table_name:
    path = 'abfss://silver@adlssmart1211.dfs.core.windows.net/SalesLT/' + name
    df = spark.read.format('delta').load(path)

    df = rename_columns_to_snake_case(df)

    output_path = 'abfss://golden@adlssmart1211.dfs.core.windows.net/SalesLT/' + name + '/'
    df.write.format('delta').mode('overwrite').save(output_path)

# COMMAND ----------

