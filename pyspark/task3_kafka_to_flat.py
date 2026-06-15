#!/usr/bin/env python3
"""Task 3: Read Kafka, flatten JSON, write flat table. Minimal."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode_outer
from pyspark.sql.types import StructType, StringType, IntegerType, ArrayType, TimestampType
import sys

SCHEMA = StructType().add("application_id", StringType()) \
    .add("customer", StructType().add("customer_id", StringType()).add("region", StringType())) \
    .add("loan", StructType().add("amount", IntegerType()).add("term_months", IntegerType())) \
    .add("scoring", StructType().add("score", IntegerType()).add("risk_level", StringType())) \
    .add("documents", ArrayType(StructType().add("type", StringType()).add("status", StringType()))) \
    .add("decision_status", StringType()) \
    .add("submitted_at", StringType())

def main():
    spark = SparkSession.builder.appName("KafkaToFlat").getOrCreate()

    if len(sys.argv) > 1 and sys.argv[1] == "--kafka":
        df = spark.read.format("kafka") \
            .option("kafka.bootstrap.servers", sys.argv[2]) \
            .option("subscribe", sys.argv[3]) \
            .load()
        value_df = df.selectExpr("CAST(value AS STRING)")
    else:
        value_df = spark.read.text(
            sys.argv[1] if len(sys.argv) > 1 else "/data/kafka_messages.jsonl"
        )

    parsed = value_df.select(from_json(col("value"), SCHEMA).alias("data")).select("data.*")

    flat = parsed.withColumn("document", explode_outer(col("documents"))) \
        .select(
            col("application_id"),
            col("customer.customer_id"),
            col("customer.region").alias("region_code"),
            col("loan.amount").alias("loan_amount"),
            col("loan.term_months"),
            col("scoring.score").alias("credit_score"),
            col("scoring.risk_level"),
            col("document.type").alias("document_type"),
            col("document.status").alias("document_status"),
            col("decision_status"),
            col("submitted_at")
        )

    output_path = sys.argv[-1] if not sys.argv[-1].startswith("--") else "/output/flat_loans.parquet"
    flat.write.mode("overwrite").parquet(output_path)

    spark.stop()

if __name__ == "__main__":
    main()
