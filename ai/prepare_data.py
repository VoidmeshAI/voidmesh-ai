# ==========================================
# FILE: ai/prepare_data.py
# ==========================================

import pandas as pd


def prepare_dataset(csv_file="reports/backtest_results.csv"):

    # ==========================================
    # LOAD CSV
    # ==========================================

    df = pd.read_csv(csv_file)

    # ==========================================
    # TARGET
    # ==========================================

    df["target"] = (df["result"] == "WIN").astype(int)

    # ==========================================
    # ENCODE TREND
    # ==========================================

    trend_map = {"BULLISH": 1, "BEARISH": -1, "SIDEWAYS": 0}

    df["trend"] = df["trend"].map(trend_map).fillna(0).astype(float)

    # ==========================================
    # ENCODE BTC STATE
    # ==========================================

    btc_map = {"STRONG_BULLISH": 1, "STRONG_BEARISH": -1, "NEUTRAL": 0}

    df["btc_state"] = df["btc_state"].map(btc_map).fillna(0).astype(float)

    # ==========================================
    # ENCODE REGIME
    # ==========================================

    regime_map = {"TRENDING": 1, "RANGING": 0, "SIDEWAYS": -1}

    df["regime"] = df["regime"].map(regime_map).fillna(0).astype(float)

    # ==========================================
    # NUMERIC SAFETY
    # ==========================================

    numeric_columns = [
        "confidence",
        "rr",
        "rsi",
        "macd",
        "macd_signal",
        "atr",
        "ema_distance",
        "volume_spike",
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ==========================================
    # DROP BAD ROWS
    # ==========================================

    df.dropna(inplace=True)

    # ==========================================
    # FEATURES
    # ==========================================

    features = [
        "confidence",
        "trend",
        "btc_state",
        "regime",
        "rr",
        "rsi",
        "macd",
        "macd_signal",
        "atr",
        "ema_distance",
        "volume_spike",
        "orderflow_bias",
        "orderflow_strength",
        "liquidity_signal",
        "liquidity_strength",
    ]

    X = df[features]

    y = df["target"]

    return X, y
