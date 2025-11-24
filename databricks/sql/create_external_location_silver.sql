CREATE EXTERNAL LOCATION extl_silver
URL 'abfss://silver@<storage-account>.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential);