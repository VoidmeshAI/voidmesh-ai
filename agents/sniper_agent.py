# ==========================================
# FILE: agents/sniper_agent.py
# ==========================================

from engines.liquidity_engine import detect_liquidity_sweep


def run_sniper_agent(df):

    liquidity = detect_liquidity_sweep(df)

    signal = liquidity["signal"]

    if "BULLISH" in signal:

        return "BUY"

    elif "BEARISH" in signal:

        return "SELL"

    return "HOLD"
