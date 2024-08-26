from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
import requests
import pandas as pd
import os

import logging

# Create a logger object
logger = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2024, 8, 25),
    # schedule="@daily",
    catchup=False,
    schedule_interval=None,
    default_args={"owner": "airflow", "retries": 0},
    tags=["crypto", "coingecko"],
    # params={
    #    "days": Param(365, type="integer", minimum=1),  # Define the days parameter with a minimum value
    # },
)
def ohlc_combined_load():
    @task
    def fetch_ohlc_data(coin_id: str, api_key: str, days: int, vs_currency: str = 'usd') -> pd.DataFrame:

        logger.info(f"Fetching OHLC data for {coin_id} for {days} days.")
        base_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
        headers = {
            "x-cg-demo-api-key": api_key
        }
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        response = requests.get(base_url, headers=headers, params=params, timeout=300)
        if response.status_code == 200:
            data = response.json()
            ohlc_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            ohlc_df['coin_id'] = coin_id
            ohlc_df['date'] = pd.to_datetime(ohlc_df['timestamp'], unit='ms')
            logger.info(f"Successfully fetched data for {coin_id}.")
            return ohlc_df
        else:
            logger.error(f"Failed to fetch data for {coin_id}: {response.status_code}")
            return pd.DataFrame()

    @task
    def prepare_sql_query(df: pd.DataFrame) -> str:
        logger.error("Prepare query")
        if df.empty:
            return ""
        values = [
            f"('{row['coin_id']}', {row['timestamp']}, {row['open']}, {row['high']}, {row['low']}, {row['close']}, '{row['date']}')"
            for _, row in df.iterrows()
        ]
        values_str = ", ".join(values)
        return f"""
        INSERT INTO ohlc_data (coin_id, timestamp, open, high, low, close, date)
        VALUES {values_str}
        ON CONFLICT (coin_id, timestamp) DO NOTHING;
        """

    @task
    def insert_data_to_neon(sql_queries: list):
        logger.info("Prepare insert_data_to_neon")
        pg_hook = PostgresHook(postgres_conn_id='neon-kit')
        for sql_query in sql_queries:
            if sql_query:
                pg_hook.run(sql_query)

    coins = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'litecoin', 'tether' 'solana', 'beam']
    logger.info(f"Started for {coins}")
    # days = "{{ params.days }}"
    days = 365
    logger.info(f"For days {days}")
    api_key = os.getenv("COIN_TOKEN")

    sql_queries = []
    for coin in coins:
        logger.info(f"Started for {coin}")
        ohlc_df = fetch_ohlc_data(coin, api_key, days)
        sql_query = prepare_sql_query(ohlc_df)
        sql_queries.append(sql_query)

    insert_data_to_neon(sql_queries)


ohlc_combined_load()
