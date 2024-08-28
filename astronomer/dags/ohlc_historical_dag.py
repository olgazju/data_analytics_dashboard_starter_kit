from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pendulum import datetime
import os
from ohlc_shared_tasks import fetch_ohlc_data, prepare_sql_query, insert_data_to_neon


@dag(
    start_date=datetime(2024, 8, 25),
    schedule_interval=None,
    catchup=False,
    default_args={"owner": "airflow", "retries": 0},
    tags=["crypto", "coingecko", "historical"],
)
def ohlc_historical_load() -> None:
    create_table_task = PostgresOperator(
        task_id='create_ohlc_table',
        postgres_conn_id='neon-kit',
        sql='schemas/create_ohlc_table.sql',
    )

    coins = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'litecoin', 'tether' 'solana', 'ripple', 'polkadot', 'dogecoin', 'usd-coin',
             'beam']

    days = 30
    api_key = os.getenv("COIN_TOKEN")

    sql_queries = []
    for coin in coins:
        ohlc_df_task = fetch_ohlc_data.override(task_id=f"fetch_ohlc_data_{coin}")(coin, api_key, days)
        sql_query_task = prepare_sql_query.override(task_id=f"prepare_sql_query_{coin}")(ohlc_df_task)
        sql_queries.append(sql_query_task)

    insert_data_task = insert_data_to_neon.override(task_id="insert_data_to_neon")(sql_queries)

    create_table_task >> sql_queries >> insert_data_task


ohlc_historical_load()
