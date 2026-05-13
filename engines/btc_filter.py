# ==========================================
# FILE: engines/btc_filter.py
# ==========================================


def btc_market_filter(trend, volatility):

    if trend == "BULLISH" and volatility != "HIGH_VOLATILITY":

        return "STRONG_BULLISH"

    elif trend == "BEARISH":

        return "STRONG_BEARISH"

    return "NEUTRAL"
