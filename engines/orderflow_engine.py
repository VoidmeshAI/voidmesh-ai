# ==========================================
# FILE: engines/orderflow_engine.py
# ==========================================


def analyze_orderflow(df):

    # ==========================================
    # BUY / SELL VOLUME
    # ==========================================

    bullish_volume = 0

    bearish_volume = 0

    recent_df = df.tail(20)

    for _, row in recent_df.iterrows():

        open_price = row["open"]

        close_price = row["close"]

        volume = row["volume"]

        # BULLISH CANDLE
        if close_price > open_price:

            bullish_volume += volume

        # BEARISH CANDLE
        else:

            bearish_volume += volume

    # ==========================================
    # PRESSURE
    # ==========================================

    total_volume = bullish_volume + bearish_volume

    if total_volume == 0:

        return {"bias": "NEUTRAL", "strength": 0}

    buy_pressure = (bullish_volume / total_volume) * 100

    sell_pressure = (bearish_volume / total_volume) * 100

    # ==========================================
    # DECISION
    # ==========================================

    if buy_pressure > 60:

        return {"bias": "BUY_PRESSURE", "strength": round(buy_pressure, 2)}

    elif sell_pressure > 60:

        return {"bias": "SELL_PRESSURE", "strength": round(sell_pressure, 2)}

    return {"bias": "NEUTRAL", "strength": 50}
