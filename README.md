# ETL yandex cloud

**Стек:** Terraform, YDB, Kafka, PySpark, Airflow, DataLens

## Структура

```
.
├── pyspark/          # PySpark скрипты
├── airflow/dags/     # Airflow DAG
├── terraform/        # Инфраструктура (YDB, Kafka, S3)
├── sql/              # SQL скрипты для YDB
└── data/             # Тестовые данные
```

## Запуск

```bash
# 1. Сгенерировать данные
python3 generate_data.py

# 2. Развернуть инфраструктуру
terraform init && terraform apply

# 3. Загрузить данные в S3
bash upload_to_s3.sh
```

## Требования

- yc (Yandex Cloud CLI)
- terraform
- python 3.8+

---

Подробности: [REPORT.md](REPORT.md)
