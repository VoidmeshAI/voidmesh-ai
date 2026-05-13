# ==========================================
# FILE: ai/features.py
# ==========================================
import math

from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
from engines.orderflow_engine import analyze_orderflow
from engines.liquidity_engine import detect_liquidity_sweep


def extract_features(df):

    # ==========================================
    # RSI
    # ==========================================

    rsi = RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]

    # ==========================================
    # MACD
    # ==========================================

    macd = MACD(close=df["close"])

    macd_value = macd.macd().iloc[-1]

    macd_signal = macd.macd_signal().iloc[-1]

    # ==========================================
    # ATR
    # ==========================================

    atr = (
        AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14)
        .average_true_range()
        .iloc[-1]
    )

    # ==========================================
    # EMA DISTANCE
    # ==========================================

    ema20 = df["close"].ewm(span=20, adjust=False).mean().iloc[-1]

    current_price = df["close"].iloc[-1]

    ema_distance = ((current_price - ema20) / current_price) * 100

    # ==========================================
    # VOLUME SPIKE
    # ==========================================

    avg_volume = df["volume"].tail(20).mean()

    current_volume = df["volume"].iloc[-1]

    volume_spike = current_volume / avg_volume

    # ==========================================
    # ORDERFLOW
    # ==========================================

    orderflow = analyze_orderflow(df)

    orderflow_bias = orderflow["bias"]

    orderflow_strength = orderflow["strength"]

    # ENCODE
    if orderflow_bias == "BUY_PRESSURE":

        orderflow_bias = 1

    elif orderflow_bias == "SELL_PRESSURE":

        orderflow_bias = -1

    else:

        orderflow_bias = 0

    # ==========================================
    # LIQUIDITY SWEEP
    # ==========================================

    liquidity = detect_liquidity_sweep(df)

    liquidity_signal = liquidity["signal"]

    liquidity_strength = liquidity["strength"]

    # ENCODE
    if liquidity_signal == "BULLISH_SWEEP":

        liquidity_signal = 1

    elif liquidity_signal == "BEARISH_SWEEP":

        liquidity_signal = -1

    else:

        liquidity_signal = 0

    # SAFETY
    if any(
        [
            math.isnan(rsi),
            math.isnan(macd_value),
            math.isnan(macd_signal),
            math.isnan(atr),
        ]
    ):
        return None

    return {
        "rsi": round(rsi, 2),
        "macd": round(macd_value, 4),
        "macd_signal": round(macd_signal, 4),
        "atr": round(atr, 4),
        "ema_distance": round(ema_distance, 4),
        "volume_spike": round(volume_spike, 2),
        "orderflow_bias": orderflow_bias,
        "orderflow_strength": round(orderflow_strength, 2),
        "liquidity_signal": liquidity_signal,
        "liquidity_strength": liquidity_strength,
    }
