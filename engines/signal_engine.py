def generate_signal(
    trend,
    btc_state,
    confidence,
    trade_allowed
):

    if not trade_allowed:
        return "HOLD"

    # BUY logic
    if (
        trend == "BULLISH"
        and btc_state == "STRONG_BULLISH"
        and confidence >= 70
    ):
        return "BUY"

    # SELL logic
    if (
        trend == "BEARISH"
        and btc_state == "STRONG_BEARISH"
        and confidence >= 70
    ):
        return "SELL"

    return "HOLD"