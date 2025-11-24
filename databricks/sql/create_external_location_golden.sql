CREATE EXTERNAL LOCATION extl_golden
URL 'abfss://golden@<storage-account>.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential);