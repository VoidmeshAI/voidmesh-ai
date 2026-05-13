# ==========================================
# FILE: engines/regime_engine.py
# ==========================================

from ta.trend import ADXIndicator


def detect_regime(df):

    # ==========================================
    # ADX TREND STRENGTH
    # ==========================================

    adx = ADXIndicator(
        high=df["high"], low=df["low"], close=df["close"], window=14
    ).adx()

    last_adx = adx.iloc[-1]

    # ==========================================
    # VOLATILITY CHECK
    # ==========================================

    recent_high = df["high"].tail(20).max()

    recent_low = df["low"].tail(20).min()

    current_price = df["close"].iloc[-1]

    volatility_percent = ((recent_high - recent_low) / current_price) * 100

    # ==========================================
    # REGIME LOGIC
    # ==========================================

    if last_adx > 25:

        return "TRENDING"

    elif volatility_percent < 1.5:

        return "SIDEWAYS"

    return "RANGING"
