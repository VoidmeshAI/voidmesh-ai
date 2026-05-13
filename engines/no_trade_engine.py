def should_trade(
    confidence,
    regime,
    volatility
):

    reasons = []

    if confidence < 65:
        reasons.append("Low confidence")

    if regime == "SIDEWAYS":
        reasons.append("Sideways market")

    if volatility == "LOW_VOLATILITY" and confidence < 75:
        reasons.append("Low volatility")

    if len(reasons) > 0:
        return False, reasons

    return True, ["Conditions acceptable"]