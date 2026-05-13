# ==========================================
# FILE: papertrade/tracker.py
# ==========================================

from rich import print

from papertrade.trades import active_trades
from papertrade.portfolio import portfolio
from papertrade.equity import equity_curve
from database.db import cursor, conn


def open_trade(symbol, signal, entry, sl, tp):

    # ==========================================
    # PREVENT DUPLICATE OPEN TRADES
    # ==========================================

    for t in active_trades:

        if t["symbol"] == symbol and t["status"] == "OPEN":

            print(f"\n[bold yellow]" f"{symbol} TRADE ALREADY OPEN" f"[/bold yellow]")

            return

    trade = {
        "symbol": symbol,
        "signal": signal,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "status": "OPEN",
    }

    active_trades.append(trade)

    cursor.execute(
        """
        INSERT INTO trades (

            symbol,
            signal,
            entry,
            sl,
            tp,
            status

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (symbol, signal, entry, sl, tp, "OPEN"),
    )

    conn.commit()

    print(f"\n[bold green]" f"TRADE OPENED: {symbol}" f"[/bold green]")


def check_trades(symbol, current_price):

    for trade in active_trades:

        if trade["symbol"] != symbol:

            continue

        if trade["status"] != "OPEN":

            continue

        # BUY
        if trade["signal"] == "BUY":

            if current_price <= trade["sl"]:

                trade["status"] = "LOSS"

                trade["close_price"] = current_price

                portfolio["current_balance"] -= 10

                portfolio["realized_pnl"] -= 10

                equity_curve.append(portfolio["current_balance"])

                print(f"\n[bold red]" f"{symbol} STOP LOSS HIT" f"[/bold red]")

            elif current_price >= trade["tp"]:

                trade["status"] = "WIN"

                trade["close_price"] = current_price

                portfolio["current_balance"] += 30

                portfolio["realized_pnl"] += 30

                equity_curve.append(portfolio["current_balance"])

                print(f"\n[bold green]" f"{symbol} TAKE PROFIT HIT" f"[/bold green]")

        # SELL
        elif trade["signal"] == "SELL":

            if current_price >= trade["sl"]:

                trade["status"] = "LOSS"

                trade["close_price"] = current_price

                portfolio["current_balance"] -= 10

                portfolio["realized_pnl"] -= 10

                equity_curve.append(portfolio["current_balance"])

                print(f"\n[bold red]" f"{symbol} STOP LOSS HIT" f"[/bold red]")

            elif current_price <= trade["tp"]:

                trade["status"] = "WIN"

                trade["close_price"] = current_price

                portfolio["current_balance"] += 30

                portfolio["realized_pnl"] += 30

                equity_curve.append(portfolio["current_balance"])

                print(f"\n[bold green]" f"{symbol} TAKE PROFIT HIT" f"[/bold green]")
