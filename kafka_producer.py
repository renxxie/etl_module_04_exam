#!/usr/bin/env python3

from kafka import KafkaProducer
import json
import sys


def main():
    bootstrap_servers = sys.argv[1] if len(sys.argv) > 1 else "localhost:9092"
    topic = sys.argv[2] if len(sys.argv) > 2 else "loan_applications"
    input_file = sys.argv[3] if len(sys.argv) > 3 else "data/kafka_messages.jsonl"

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    count = 0
    with open(input_file) as f:
        for line in f:
            data = json.loads(line)
            producer.send(topic, value=data)
            count += 1

    producer.flush()


if __name__ == "__main__":
    main()
