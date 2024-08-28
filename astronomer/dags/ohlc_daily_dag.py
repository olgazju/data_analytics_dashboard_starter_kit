from airflow.decorators import dag
from pendulum import datetime
from ohlc_shared_tasks import fetch_ohlc_data, prepare_sql_query, insert_data_to_neon
import os


@dag(
    start_date=datetime(2024, 8, 25),
    schedule_interval="@daily",
    catchup=False,
    default_args={"owner": "airflow", "retries": 0},
    tags=["crypto", "coingecko"],
)
def ohlc_daily_load() -> None:
    coins = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'litecoin', 'tether' 'solana', 'ripple', 'polkadot', 'dogecoin', 'usd-coin',
             'beam']
    days = 1
    api_key = os.getenv("COIN_TOKEN")

    sql_queries = []
    for coin in coins:
        ohlc_df_task = fetch_ohlc_data.override(task_id=f"fetch_ohlc_data_{coin}")(coin, api_key, days)
        sql_query_task = prepare_sql_query.override(task_id=f"prepare_sql_query_{coin}")(ohlc_df_task)
        sql_queries.append(sql_query_task)

    insert_data_task = insert_data_to_neon.override(task_id="insert_data_to_neon")(sql_queries)

    sql_queries >> insert_data_task


ohlc_daily_load()
