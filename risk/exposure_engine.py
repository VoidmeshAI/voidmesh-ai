# ==========================================
# FILE: risk/exposure_engine.py
# ==========================================

from papertrade.trades import active_trades


def check_portfolio_exposure():

    # ==========================================
    # OPEN TRADES
    # ==========================================

    open_trades = []

    for trade in active_trades:

        if trade["status"] == "OPEN":

            open_trades.append(trade)

    total_open = len(open_trades)

    # ==========================================
    # MAX POSITIONS
    # ==========================================

    if total_open >= 5:

        return {"allowed": False, "reason": "MAX_POSITIONS_REACHED"}

    # ==========================================
    # BUY / SELL EXPOSURE
    # ==========================================

    buy_positions = 0

    sell_positions = 0

    for trade in open_trades:

        if trade["signal"] == "BUY":

            buy_positions += 1

        elif trade["signal"] == "SELL":

            sell_positions += 1

    # ==========================================
    # OVEREXPOSURE
    # ==========================================

    if buy_positions >= 4:

        return {"allowed": False, "reason": "TOO_MANY_BUYS"}

    if sell_positions >= 4:

        return {"allowed": False, "reason": "TOO_MANY_SELLS"}

    # ==========================================
    # SAFE
    # ==========================================

    return {"allowed": True, "reason": "SAFE"}
