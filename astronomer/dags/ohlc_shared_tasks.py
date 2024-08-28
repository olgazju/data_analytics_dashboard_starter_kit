from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import pandas as pd
import logging

logger = logging.getLogger("airflow.task")


@task
def fetch_ohlc_data(coin_id: str, api_key: str, days: int, vs_currency: str = 'usd') -> pd.DataFrame:
    """
    Fetches OHLC (Open, High, Low, Close) data for a given cryptocurrency.

    Args:
        coin_id (str): The ID of the cryptocurrency to fetch data for.
        api_key (str): The API key for authentication with the data provider.
        days (int): Number of days for which to fetch the data.
        vs_currency (str): The currency to use for comparison (default is 'usd').

    Returns:
        pd.DataFrame: A DataFrame containing the OHLC data.
    """
    logger.info(f"Fetching OHLC data for {coin_id} for {days} days.")
    base_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    headers = {"x-cg-demo-api-key": api_key}
    params = {"vs_currency": vs_currency, "days": days}
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
    """
    Prepares an SQL query for inserting OHLC data into the database.

    Args:
        df (pd.DataFrame): The DataFrame containing OHLC data.

    Returns:
        str: An SQL query string for inserting the data.
    """
    logger.info("Preparing SQL query")
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
def insert_data_to_neon(sql_queries: list[str]) -> None:
    """
    Inserts OHLC data into the Neon PostgreSQL database.

    Args:
        sql_queries (list[str]): A list of SQL queries to execute.
    """
    logger.info("Inserting data to Neon PostgreSQL")
    pg_hook = PostgresHook(postgres_conn_id='neon-kit')
    for sql_query in sql_queries:
        if sql_query:
            pg_hook.run(sql_query)


def load_ohlc_data(coins: list[str], days: int, api_key: str) -> None:
    """
    Loads OHLC data for a list of cryptocurrencies for a given number of days.

    Args:
        coins (list[str]): A list of cryptocurrency coin IDs.
        days (int): Number of days for which to fetch OHLC data.
        api_key (str): API key for authentication with the data provider.
    """
    sql_queries = []
    for coin in coins:
        ohlc_df = fetch_ohlc_data(coin, api_key, days)
        sql_query = prepare_sql_query(ohlc_df)
        sql_queries.append(sql_query)
    insert_data_to_neon(sql_queries)
