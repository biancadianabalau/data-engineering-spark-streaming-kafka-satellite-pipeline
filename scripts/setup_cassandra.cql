-- 1. Create data base
CREATE KEYSPACE IF NOT EXISTS satellite_ks 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- 2. 
USE satellite_ks;

-- 3. Create table
CREATE TABLE IF NOT EXISTS alerts (
    satid bigint,
    satname text,
    latitude double,
    longitude double,
    altitude double,
    timestamp bigint,
    PRIMARY KEY (satid, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
