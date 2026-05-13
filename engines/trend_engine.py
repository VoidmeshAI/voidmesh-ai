# ==========================================
# FILE: engines/trend_engine.py
# ==========================================

from ta.trend import EMAIndicator


def get_trend(df):

    ema20 = EMAIndicator(close=df["close"], window=20).ema_indicator()

    ema50 = EMAIndicator(close=df["close"], window=50).ema_indicator()

    last_ema20 = ema20.iloc[-1]

    last_ema50 = ema50.iloc[-1]

    if last_ema20 > last_ema50:

        return "BULLISH"

    elif last_ema20 < last_ema50:

        return "BEARISH"

    return "SIDEWAYS"
