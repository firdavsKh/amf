from datetime import datetime, timedelta
from datetime import date
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from apache.airflow.providers.clickhouse.operators.ClickhouseOperator import ClickhouseOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
# from pathlib import Path
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

dag = DAG(
    dag_id='example_clickhouse_operator',
    start_date = days_ago(0,0,0,0), 
    # schedule_interval = timedelta(seconds=30),
    catchup=False,
    template_searchpath='$AIRFLOW_HOME/include'
)

def get_hello(**kwargs): 
    ti = kwargs['ti']
    df = pd.DataFrame(pd.read_csv(f'{CUR_DIR}/files/student1.csv'))
    arr = []
    for i in range(len(df)):
        arr.append(f"'{df['Name'][i]}',{df['Age'][i]},'{df['marks'][i]}','{df['date'][i]}'")
    arr = tuple(arr)
    mass = "),(".join(map(str,arr))
    ti.xcom_push(key='mVariable', value=mass)
    ls = ti.xcom_pull(key='mVariable',task_ids=['get_hello'])
    print(ls)


firstOper = PythonOperator(
    task_id = 'get_hello',
    python_callable = get_hello,
    provide_context=True, 
    dag = dag 
)

    # run_this_last = DummyOperator(task_id='run_this_last')
    # load sql from file
    # set sql direct in the code section
select_push = ClickhouseOperator(
    task_id='select_xcom',
    sql="INSERT INTO t1 (*) VALUES({{ti.xcom_pull(key='mVariable',task_ids=['get_hello'])[0]}})", 
    click_conn_id='myConnect',
    dag=dag,
)


    
firstOper>>select_push



