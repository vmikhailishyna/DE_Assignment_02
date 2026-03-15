from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import Variable
from datetime import datetime, timedelta
import logging
import duckdb
import pymysql
import json
import os

JSON_DIR = '/usr/local/airflow/dags/telephony_api_mocks'
DUCKDB_PATH = '/usr/local/airflow/dags/support_analytics.db'
logger = logging.getLogger('airflow')

def detect_new_calls_fn(ti):
    last_loaded_call_time = Variable.get('last_calls', default_var="2026-01-01 00:00:00")
    mysql_hook = MySqlHook(mysql_conn_id='mysql_support_call_center')

    sql_query = f"""
    Select c.call_id, c.employee_id, e.full_name, e.team, c.call_time, c.phone, c.direction, c.status
    FROM calls c
    JOIN employees e ON c.employee_id = e.employee_id
    WHERE c.call_time > '{last_loaded_call_time}'
    """

    records = mysql_hook.get_records(sql_query)
    if not records:
        return []

    calls = []
    for record in records:
        calls.append({
            'call_id': record[0], 'employee_id': record[1], 'full_name': record[2],
            'team': record[3], 'call_time': str(record[4]), 'phone': record[5], 'direction': record[6],
            'status': record[7]
        })
    logger.info(f"[detect_new_calls] New calls detected: {len(calls)}")
    logger.info(f"[detect_new_calls] Watermark: {last_loaded_call_time}")
    return calls

def load_telephony_details_fn(ti):
    calls = ti.xcom_pull(task_ids='detect_new_calls')
    if not calls:
        return []

    enrich_calls = []
    for call in calls:
        file_path = f'{JSON_DIR}/call_{call["call_id"]}.json'
        if os.path.exists(file_path):
            with open(file_path) as json_file:
                data = json.load(json_file)
                call['duration_sec'] = data['duration_sec']
                call['short_description'] = data['short_description']
                enrich_calls.append(call)
        else:
            print(f"{file_path} not found.")

    reject_calls = len(calls) - len(enrich_calls)
    logger.info(f"[load_telephony_details] Calls: {len(calls)}")
    logger.info(f"[load_telephony_details] Enrich calls: {len(enrich_calls)}")
    logger.info(f"[load_telephony_details] Rejects: {reject_calls}")

    return enrich_calls

def transform_and_load_duckdb_fn(ti):
    data = ti.xcom_pull(task_ids='load_telephony_details')
    if not data:
        return []

    db = duckdb.connect(DUCKDB_PATH)

    db.execute("""
    Create table if not exists support_calls(
    call_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    full_name VARCHAR,
    team VARCHAR,
    call_time TIMESTAMP,
    phone VARCHAR,
    direction VARCHAR,
    status VARCHAR,
    duration_sec INTEGER,
    short_description TEXT)
    """)


    for call in data:
        db.execute("""
        INSERT OR REPLACE INTO support_calls
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (call['call_id'], call['employee_id'], call['full_name'],
              call['team'], call['call_time'], call['phone'], call['direction'],
              call['status'], call['duration_sec'], call['short_description']))

    last_loaded_call_time = max([call['call_time'] for call in data])
    Variable.set('last_calls', last_loaded_call_time)

    logger.info(f"[transform_and_load_duckdb] Get data: {len(data)}")
    logger.info(f"[transform_and_load_duckdb] last_loaded_call_time: {last_loaded_call_time}")
    db.close()




default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 3, 12),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    "support_dag",
    default_args=default_args,
    schedule="@hourly",
    catchup=True,
    max_active_runs = 1
)

detect_new_calls = PythonOperator(
    task_id='detect_new_calls',
    python_callable=detect_new_calls_fn,
    dag=dag
)

load_telephony_details = PythonOperator(
    task_id='load_telephony_details',
    python_callable=load_telephony_details_fn,
    dag=dag
)

transform_and_load_duckdb_fn = PythonOperator(
    task_id='transform_and_load_duckdb',
    python_callable=transform_and_load_duckdb_fn,
    dag=dag
)

detect_new_calls >> load_telephony_details >> transform_and_load_duckdb_fn
