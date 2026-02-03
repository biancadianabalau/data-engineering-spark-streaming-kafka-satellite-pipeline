in progress
# Real-Time Satellite Geo-Fencing Pipeline
Real-time Data Engineering pipeline tracking satellites via N2YO API. Uses Python &amp; Apache Kafka for ingestion, Spark Structured Streaming for geo-fencing, and a dual-storage strategy: Delta Lake for ACID transactions and Apache Cassandra for NoSQL real-time access. Fully containerized with Docker.

## 🏗️ Architecture
Data Source: N2YO API (Real-time orbital data).

Ingestion Layer: Python-based Kafka Producer.

Message Broker: Apache Kafka (Distributed streaming platform).

Stream Processing: Apache Spark Structured Streaming (Geo-fencing logic & transformations).

Storage (Hot Path): Apache Cassandra (NoSQL database for low-latency alerts).

Storage (Cold Path): Delta Lake / Parquet (ACID transactions on top of a Data Lake).

Infrastrucure: Fully containerized using Docker & Docker Compose.


## 🛠️ Tech Stack
Language: Python 3.x

Streaming: Apache Spark 3.5.0, Apache Kafka

Storage: Apache Cassandra, Delta Lake 3.0.0

Containerization: Docker & Docker Compose



## 🚀 How to Run
1. Clone the repo.
2. Run `docker-compose up -d`.
3. Create the Cassandra schema (commands in `/scripts`).
4. Start ingestion: `python ingestion.py`.
5. Submit Spark Job: `docker exec -it spark-master spark-submit ...`

## 📊 Data Analysis & Insights
The pipeline successfully captures satellite data when it enters the predefined bounding box (Europe/Romania).

Example Insights captured:

Starlink Satellites: Account for over 70% of the tracked traffic.

Processing Latency: Average end-to-end latency from API to Cassandra is under 2 seconds.


