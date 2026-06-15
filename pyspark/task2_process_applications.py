#!/usr/bin/env python3
"""Task 2: Process applications.csv with PySpark. Minimal, direct."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date, trunc
import sys

def main():
    spark = SparkSession.builder.appName("ProcessApplications").getOrCreate()

    df = spark.read.csv(
        sys.argv[1] if len(sys.argv) > 1 else "/data/applications.csv",
        header=True,
        inferSchema=True
    )

    result = df.groupBy(
        to_date(col("event_time")).alias("date"),
        col("region_code")
    ).agg({
        "application_id": "count",
        "requested_amount": "sum",
        "approved_amount": "sum"
    }).select(
        col("date"),
        col("region_code"),
        col("count(application_id)").alias("total_applications"),
        col("sum(requested_amount)").alias("total_requested"),
        col("sum(approved_amount)").alias("total_approved"),
        (col("sum(approved_amount)") / col("sum(requested_amount)")).alias("approval_rate")
    )

    result.write.mode("overwrite").parquet(
        sys.argv[2] if len(sys.argv) > 2 else "/output/aggregated_applications.parquet"
    )

    spark.stop()

if __name__ == "__main__":
    main()
