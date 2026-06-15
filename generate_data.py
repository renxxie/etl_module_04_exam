#!/usr/bin/env python3

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

REGIONS = ["DE-HE", "DE-BY", "DE-NW", "DE-BW", "DE-SN"]
CAMPAIGN_TYPES = ["credit_card_offer", "loan_refinance", "insurance_cross_sell"]
CALL_STATUSES = ["answered", "no_answer", "voicemail", "busy"]
CLIENT_RESPONSES = ["interested", "not_interested", "call_back_later", "interested_urg"]
PRODUCT_TYPES = ["cash_loan", "mortgage", "credit_card", "auto_loan"]
DECISION_STATUSES = ["approved", "rejected", "manual_review", "pending"]
RISK_LEVELS = ["low", "medium", "high"]
CHANNELS = ["mobile", "web", "branch", "call_center"]
DOC_TYPES = ["passport", "income_statement", "employment_proof", "property_deed"]
DOC_STATUSES = ["verified", "pending", "rejected"]


def generate_transactions(num_rows: int, output_path: Path) -> None:
    start = datetime(2026, 5, 1, 9, 0, 0)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "call_id",
                "call_time",
                "client_id",
                "region_code",
                "campaign_type",
                "call_status",
                "client_response",
                "duration_sec",
                "follow_up_required",
            ]
        )

        for i in range(num_rows):
            call_time = start + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 11),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )

            writer.writerow(
                [
                    f"call_20260501_{i + 1:04d}",
                    call_time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"client_{random.randint(1000, 9999)}",
                    random.choice(REGIONS),
                    random.choice(CAMPAIGN_TYPES),
                    random.choice(CALL_STATUSES),
                    random.choice(CLIENT_RESPONSES) if random.random() > 0.3 else "",
                    random.randint(30, 600),
                    str(random.random() > 0.7).lower(),
                ]
            )


def generate_applications(num_rows: int, output_path: Path) -> None:
    start = datetime(2026, 5, 1, 9, 0, 0)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "application_id",
                "event_time",
                "customer_id",
                "region_code",
                "product_type",
                "requested_amount",
                "term_months",
                "credit_score",
                "risk_level",
                "decision_status",
                "approved_amount",
                "channel",
                "employee_review_flag",
                "processing_time_sec",
            ]
        )

        for i in range(num_rows):
            event_time = start + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 14),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )

            req_amount = random.choice([5000, 10000, 15000, 20000, 25000, 50000])
            decision = random.choice(DECISION_STATUSES)
            approved = req_amount if decision == "approved" else 0

            writer.writerow(
                [
                    f"app_20260501_{i + 1:04d}",
                    event_time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"cust_{random.randint(10000, 99999)}",
                    random.choice(REGIONS),
                    random.choice(PRODUCT_TYPES),
                    req_amount,
                    random.choice([12, 24, 36, 48, 60]),
                    random.randint(300, 850),
                    random.choice(RISK_LEVELS),
                    decision,
                    approved,
                    random.choice(CHANNELS),
                    str(decision == "manual_review").lower(),
                    random.randint(5, 120),
                ]
            )


def generate_kafka_messages(num_rows: int, output_path: Path) -> None:
    start = datetime(2026, 5, 1, 10, 0, 0)

    with open(output_path, "w") as f:
        for i in range(num_rows):
            submitted_at = start + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 14),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )

            num_docs = random.randint(1, 3)
            documents = [
                {
                    "type": random.choice(DOC_TYPES),
                    "status": random.choice(DOC_STATUSES),
                }
                for _ in range(num_docs)
            ]

            message = {
                "application_id": f"loan_{random.randint(100000, 999999)}",
                "customer": {
                    "customer_id": f"cust_{random.randint(100, 999)}",
                    "region": random.choice(REGIONS),
                },
                "loan": {
                    "amount": random.choice([5000, 10000, 15000, 20000, 25000]),
                    "term_months": random.choice([12, 24, 36, 48, 60]),
                },
                "scoring": {
                    "score": random.randint(300, 850),
                    "risk_level": random.choice(RISK_LEVELS),
                },
                "documents": documents,
                "decision_status": random.choice(DECISION_STATUSES),
                "submitted_at": submitted_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            f.write(json.dumps(message) + "\n")


def main():
    base = Path("/Users/xtsu/Desktop/etl_final/data")
    base.mkdir(exist_ok=True)

    generate_transactions(250000, base / "transactions.csv")
    generate_applications(400000, base / "applications.csv")
    generate_kafka_messages(150000, base / "kafka_messages.jsonl")


if __name__ == "__main__":
    main()
