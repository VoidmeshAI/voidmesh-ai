# ==========================================
# FILE: engines/liquidity_engine.py
# ==========================================


def detect_liquidity_sweep(df):

    recent_high = df["high"].tail(20).max()

    recent_low = df["low"].tail(20).min()

    current_high = df["high"].iloc[-1]

    current_low = df["low"].iloc[-1]

    current_close = df["close"].iloc[-1]

    # ==========================================
    # BEARISH SWEEP
    # ==========================================

    if current_high > recent_high and current_close < recent_high:

        return {"signal": "BEARISH_SWEEP", "strength": 80}

    # ==========================================
    # BULLISH SWEEP
    # ==========================================

    if current_low < recent_low and current_close > recent_low:

        return {"signal": "BULLISH_SWEEP", "strength": 80}

    return {"signal": "NO_SWEEP", "strength": 0}
