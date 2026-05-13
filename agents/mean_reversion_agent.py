# ==========================================
# FILE: agents/mean_reversion_agent.py
# ==========================================


def run_mean_reversion_agent(df):

    close = df["close"].iloc[-1]

    sma = df["close"].rolling(20).mean().iloc[-1]

    if close > sma * 1.01:

        return "SELL"

    elif close < sma * 0.99:

        return "BUY"

    return "HOLD"
