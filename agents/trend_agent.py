# ==========================================
# FILE: agents/trend_agent.py
# ==========================================

from engines.trend_engine import get_trend


def run_trend_agent(df):

    trend = get_trend(df)

    if trend == "BULLISH":

        return "BUY"

    elif trend == "BEARISH":

        return "SELL"

    return "HOLD"
