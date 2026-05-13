# ==========================================
# FILE: risk/leverage_engine.py
# ==========================================


def calculate_leverage(ai_probability, volatility, regime):

    leverage = 2

    # ==========================================
    # AI PROBABILITY
    # ==========================================

    if ai_probability >= 85:

        leverage += 5

    elif ai_probability >= 75:

        leverage += 3

    elif ai_probability >= 65:

        leverage += 2

    # ==========================================
    # VOLATILITY
    # ==========================================

    if volatility == "HIGH_VOLATILITY":

        leverage -= 2

    # ==========================================
    # REGIME
    # ==========================================

    if regime == "TRENDING":

        leverage += 1

    elif regime == "SIDEWAYS":

        leverage -= 1

    # ==========================================
    # SAFETY
    # ==========================================

    leverage = max(1, min(leverage, 10))

    return leverage
