from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.yandex.operators.dataproc import DataprocPySparkOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 6, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "etl_applications",
    default_args=default_args,
    description="desc",
    schedule_interval=None,
    catchup=False,
    tags=[],
)

create_cluster = BashOperator(
    task_id="create_cluster",
    bash_command="""
    yc dataproc cluster create \
      --name etl-cluster-{{ ds_nodash }} \
      --zone ru-central1-a \
      --service-account-id {{ var.value.YC_SA_ID }} \
      --cluster-config \
        ssh publicKey={{ var.value.SSH_PUBLIC_KEY }},\
        version=2.0,\
        services='["yarn","spark","hdfs"]',\
        subcluster-specs='[{"name":"master","resource-preset":"s2.small","hosts-count":1,"zone-id":"ru-central1-a"},{"name":"compute","resource-preset":"s2.small","hosts-count":2,"zone-id":"ru-central1-a"}]'
    """,
    dag=dag,
)

run_pyspark = BashOperator(
    task_id="run_pyspark",
    bash_command="""
    SUBMISSION_ID=$(yc dataproc job pyspark create \
      --cluster-id $(yc dataproc cluster get etl-cluster-{{ ds_nodash }} --format json | jq -r '.id') \
      --name process-applications \
      --main-python-file-uri /data/task2_process_applications.py \
      --args /data/applications.csv,/output/aggregated_applications.parquet \
      --format json | jq -r '.id')
    echo $SUBMISSION_ID
    yc dataproc job wait $SUBMISSION_ID
    """,
    dag=dag,
)

delete_cluster = BashOperator(
    task_id="delete_cluster",
    bash_command="yc dataproc cluster delete --name etl-cluster-{{ ds_nodash }} --async",
    dag=dag,
    trigger_rule="all_done",
)

create_cluster >> run_pyspark >> delete_cluster
