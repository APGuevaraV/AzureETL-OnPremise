CREATE EXTERNAL LOCATION extl_bronze
URL 'abfss://bronze@<storage-account>.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential);