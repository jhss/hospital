from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.utils.dates import days_ago
from src.data_ingest import data_ingest
from src.transform import transform
from datetime import datetime, timedelta
import os

now = datetime.now()

AIRFLOW_HOME = os.environ['AIRFLOW_HOME']
default_args = {
    'owner': 'default_user',
    'start_date': datetime(now.year, now.month, now.day),
    'retries': 1,
    'retry_delay': timedelta(minutes=60),
}

dag = DAG(dag_id='ETL',
          default_args = default_args,
          schedule_interval=timedelta(days=1),)


start = DummyOperator(task_id = 'start', dag = dag)

#t1 = PythonOperator(task_id='data_ingest',
#                    python_callable = data_ingest,
#                    dag = dag)
h1 = BashOperator(
        task_id = 'mkdir',
        bash_command = "/opt/hadoop/bin/hdfs dfs -mkdir -p /hospital/data",
        dag = dag
        )

h2 = BashOperator(
        task_id = 'load_to_hdfs',
        bash_command = f"/opt/hadoop/bin/hdfs dfs -put -f {AIRFLOW_HOME}/dags/data/HospitalEvaluation.csv /hospital/data/HospitalEvaluation.csv",
        dag = dag
        )

h3 = BashOperator(
        task_id = 'load_to_hdfs2',
        bash_command = f"/opt/hadoop/bin/hdfs dfs -put -f {AIRFLOW_HOME}/dags/data/HospitalTreatment.csv /hospital/data/HospitalTreatment.csv",
        dag = dag
        )


spark_config = {
    "spark.master": "yarn",
}

'''
spark_job = SparkSubmitOperator(
    task_id = 'data_transform',
    application="/home/airflow/dags/src/data_transform.py",
    name = "data_transform",
    conf = spark_config,
    verbose=1,
    dag = dag
)
'''
spark_job = PythonOperator(task_id = 'transform_and_persist',
                           provide_context=True,
                           python_callable=transform,
                           dag = dag)

start >> h1 >> h2>> h3 >> spark_job
