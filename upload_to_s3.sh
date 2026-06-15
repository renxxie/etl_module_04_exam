#!/bin/bash
set -e

BUCKET="dvlgerasimenko-etl-bucket"

yc storage s3 cp data/transactions.csv "s3://$BUCKET/transactions/transactions.csv"
yc storage s3 cp data/applications.csv "s3://$BUCKET/applications/applications.csv"
yc storage s3 cp data/kafka_messages.jsonl "s3://$BUCKET/kafka/kafka_messages.jsonl"
yc storage s3 ls "s3://$BUCKET/" --recursive
