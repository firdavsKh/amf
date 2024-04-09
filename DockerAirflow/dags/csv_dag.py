import datetime
import time
import requests
import pandas as pd
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import pathlib
import os
import sys
import pandas as pd
import json
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
import clickhouse_connect
our_second_dag = DAG(
    "A_example_csv_dag",
    start_date = days_ago(0,0,0,0)
)
def misol1(**kwargs):
    # df = pd.read_csv('https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv')
    df = pd.DataFrame([['Alice', 30, 'New York'], ['Bob', 25, 'Los Angeles']], columns=['Name', 'Age', 'City'])
    # print(df)
    # print(pathlib.Path(__file__))
    # df.to_csv("df.csv")
    df = pd.DataFrame(df) 
    # print('!!!!!!!!!!!!!!!!!!!!!!')
    # print(type(df))
    # print(df)
    ti = kwargs['ti']
    ti.xcom_push(key='mVariable', value=df)
    # expense_variable = context['task_instance'].xcom_pull(task_ids='expense_list')

firstOper = PythonOperator(
    task_id = 'misol1',
    python_callable = misol1,
    provide_context=True,
    dag = our_second_dag 
)

def misol2(**kwargs):
    # gr = pd.read_csv('df.csv')
    ti = kwargs['ti']
    ls = ti.xcom_pull(key='mVariable',task_ids=['misol1'])
    print('this!!!!!!!!!!!!!!!!!!!!!!!')
    print(ls)
    ls = pd.DataFrame(ls)
    
    ls.to_csv("hello.csv")


secondOper = PythonOperator(
    task_id = 'misol2',
    python_callable = misol2,
    provide_context=True,
    dag = our_second_dag 
)  


# os.chdir("/usr/local/airflow/dags/")
# C:\Users\Pirov M\Documents\production\DockerAirflow\dags\csv_dag.py

firstOper>>secondOper