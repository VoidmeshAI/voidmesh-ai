# ==========================================
# FILE: backtest/equity.py
# ==========================================


def build_equity_curve(results, starting_balance=1000, risk_per_trade=0.01):

    balance = starting_balance

    equity_curve = []

    peak_balance = balance

    max_drawdown = 0

    for r in results:

        rr_result = r["rr_result"]

        risk_amount = balance * risk_per_trade

        pnl = risk_amount * rr_result

        balance += pnl

        # SAVE EQUITY
        equity_curve.append(balance)

        # DRAWDOWN
        if balance > peak_balance:

            peak_balance = balance

        drawdown = ((peak_balance - balance) / peak_balance) * 100

        max_drawdown = max(max_drawdown, drawdown)

    return {
        "final_balance": round(balance, 2),
        "equity_curve": equity_curve,
        "max_drawdown": round(max_drawdown, 2),
    }
