# ==========================================
# FILE: engines/probability_engine.py
# ==========================================


def calculate_confidence(trend, btc_state, volatility, regime):

    confidence = 50

    reasons = []

    # ==========================================
    # TREND
    # ==========================================

    if trend == "BULLISH":

        confidence += 8

        reasons.append("Bullish market trend detected")

    elif trend == "BEARISH":

        confidence += 8

        reasons.append("Bearish market trend detected")

    # ==========================================
    # BTC MARKET
    # ==========================================

    if btc_state == "STRONG_BULLISH":

        confidence += 10

        reasons.append("BTC market strength bullish")

    elif btc_state == "STRONG_BEARISH":

        confidence += 10

        reasons.append("BTC market bearish pressure")

    # ==========================================
    # VOLATILITY
    # ==========================================

    if volatility == "HIGH_VOLATILITY":

        confidence -= 10

        reasons.append("High volatility risk")

    elif volatility == "LOW_VOLATILITY":

        confidence += 3

        reasons.append("Stable volatility conditions")

    # ==========================================
    # REGIME
    # ==========================================

    if regime == "TRENDING":

        confidence += 10

        reasons.append("Trending market structure")

    elif regime == "SIDEWAYS":

        confidence -= 10

        reasons.append("Sideways market detected")

    # ==========================================
    # SAFETY
    # ==========================================

    confidence = max(0, min(confidence, 100))

    return confidence, reasons
