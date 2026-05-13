# ==========================================
# FILE: data/market_data.py
# ==========================================

import pandas as pd

from data.binance_client import get_klines


def get_dataframe(symbol="BTCUSDT", interval="15m", limit=200):

    # FETCH KLINES
    klines = get_klines(symbol=symbol, interval=interval, limit=limit)

    # DATAFRAME
    df = pd.DataFrame(
        klines,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )

    # ==========================================
    # CONVERT TYPES
    # ==========================================

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_asset_volume",
        "taker_buy_base",
        "taker_buy_quote",
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(df[col], errors="coerce")

    # TIME
    df["time"] = pd.to_numeric(df["time"], errors="coerce")

    # DROP BAD ROWS
    df.dropna(inplace=True)

    # RESET INDEX
    df.reset_index(drop=True, inplace=True)

    return df
