from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

spark = SparkSession.builder \
    .appName("SatelliteDeltaPipeline") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()
    
schema = StructType([
    StructField("satid", LongType(), True),
    StructField("satname", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("altitude", DoubleType(), True),
    StructField("timestamp", LongType(), True)
])

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "satellite_stream") \
    .option("startingOffsets", "earliest") \
    .load()


json_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

europe_df = json_df.filter(
    (col("latitude") >= 35.0) & (col("latitude") <= 70.0) &
    (col("longitude") >= -25.0) & (col("longitude") <= 45.0)
)


query_console = europe_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query_delta = europe_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/opt/spark/checkpoint/delta_alerts") \
    .start("/opt/spark/delta_europe_data")

query_cassandra = europe_df.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "satellite_ks") \
    .option("table", "alerts") \
    .option("checkpointLocation", "/opt/spark/checkpoint/cassandra_alerts") \
    .outputMode("append") \
    .start()

spark.streams.awaitAnyTermination()
