# ==========================================
# FILE: risk/position_sizing.py
# ==========================================


def calculate_position_size(balance, risk_percent, entry, sl, leverage=1):

    # ==========================================
    # RISK AMOUNT
    # ==========================================

    risk_amount = (balance * risk_percent) / 100

    # ==========================================
    # STOP DISTANCE
    # ==========================================

    stop_distance = abs(entry - sl)

    if stop_distance == 0:

        return 0

    # ==========================================
    # POSITION SIZE
    # ==========================================

    quantity = risk_amount / stop_distance

    # ==========================================
    # LEVERAGE
    # ==========================================

    quantity *= leverage

    return round(quantity, 3)
