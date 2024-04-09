from airflow.providers.http.operators.http import SimpleHttpOperator
import datetime
# import time
# import requests
# import pandas as pd
from airflow import DAG
# from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
# from airflow.models import Variable
# import pathlib
# import os
# import sys
# import pandas as pd
http_dag = DAG(
    "misol_http",
    start_date = days_ago(0,0,0,0)
)
# # Define the task
http_task = SimpleHttpOperator(
    task_id='perform_http_request',
    method='GET',
    http_conn_id='http_default',
    endpoint='api/v1/resource',
    headers={'Content-Type': 'application/json'},
    # xcom_push=True,
    dag = http_dag
)

http_task