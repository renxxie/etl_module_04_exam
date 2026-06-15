## Реализация

### 1. Yandex DataTransfer

**Архитектура:**
```
YDB → Data Transfer → Object Storage → DataLens
```

**Компоненты:**
- Serverless YDB база данных
- Object Storage бакет (S3 API)
- Service Account с правами storage.editor, ydb.editor

**Скрипты:**
- `ydb-to-object-storage.tf` — Terraform конфигурация
- `sql/01_create_table.sql` — создание таблицы
- `sql/02_bulk_insert.sql` — загрузка данных

**Результат:**
- Объем данных: 25.3 MB
- Записей: 250,000 транзакций

---

### 2. Data Processing + Airflow

**Архитектура:**
```
S3 → Dataproc Cluster → PySpark Job → Parquet → DataLens
                       ↓
                   Airflow DAG
```

**Компоненты:**
- PySpark для агрегации данных
- Airflow DAG для управления кластером
- Автоматическое создание/удаление кластера

**Скрипты:**
- `pyspark/task2_process_applications.py` — PySpark job
- `airflow/dags/etl_dag.py` — Airflow DAG

**Workflow:**
1. create_cluster
2. run_pyspark
3. delete_cluster

**Результат:**
- Объем данных: 44.1 MB
- Записей: 400,000 заявок

---

### 3. Kafka + PySpark

**Архитектура:**
```
Producer → Kafka → PySpark Structured Streaming → Parquet
```

**Компоненты:**
- Apache Kafka кластер (3 брокера)
- Kafka Producer для отправки сообщений
- PySpark для обработки потока данных

**Скрипты:**
- `terraform/kafka.tf` — конфигурация Kafka
- `kafka_producer.py` — producer
- `pyspark/task3_kafka_to_flat.py` — stream processing

**Обработка:**
- Парсинг JSON из Kafka
- Flattening вложенных структур
- Запись в плоскую таблицу

**Результат:**
- Объем данных: 53.5 MB
- Сообщений: 150,000

---

### 4. DataLens

**Подключение:**
- Тип: S3-compatible
- Endpoint: storage.yandexcloud.net
- Формат: Parquet

**Дашборды:**

1. **Applications Performance**
   - График заявок по датам и регионам
   - Approval rate по регионам
   - Распределение risk levels

2. **Loan Portfolio Analytics**
   - Гистограмма сумм кредитов
   - Статус верификации документов
   - Зависимость credit score от суммы

---

## Структура проекта

```
etl_final/
├── pyspark/                    # PySpark скрипты
├── airflow/dags/               # Airflow DAG
├── terraform/                  # Инфраструктура
├── sql/                        # SQL скрипты
└── data/                       # Тестовые данные
```

---

## Технологический стек

| Компонент | Технология |
|-----------|------------|
| IaC | Terraform |
| Database | YDB Serverless |
| Data Lake | Object Storage |
| Batch Processing | PySpark |
| Orchestration | Apache Airflow |
| Streaming | Apache Kafka |
| Visualization | Yandex DataLens |
