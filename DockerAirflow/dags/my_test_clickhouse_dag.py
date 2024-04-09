# from datetime import datetime, timedelta

# from airflow import DAG
# from airflow.operators.dummy import DummyOperator
# from airflow.utils.dates import days_ago
# from apache.airflow.providers.clickhouse.operators.ClickhouseOperator import ClickhouseOperator 

# default_args = {
#     'start_date': days_ago(0,0,0,0),
# }
# dag = DAG('clickhouse_integration', default_args=default_args, schedule_interval='@daily')

# insert_task = ClickhouseOperator(
#     task_id='insert_data',
#     clickhouse_conn_id='myConnect',
#     sql='INSERT INTO table VALUES ...',
#     dag=dag
# )
# insert_task