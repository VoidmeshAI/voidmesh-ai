# ==========================================
# FILE: reports/daily_report.py
# ==========================================

from database.db import cursor

from papertrade.portfolio import portfolio

from telegram.send_message import send_telegram_message


def send_daily_report():

    # ==========================================
    # TOTAL TRADES
    # ==========================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM trades
""")

    total_trades = cursor.fetchone()[0]

    # ==========================================
    # WINS
    # ==========================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM trades
        WHERE status = 'WIN'
""")

    wins = cursor.fetchone()[0]

    # ==========================================
    # LOSSES
    # ==========================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM trades
        WHERE status = 'LOSS'
""")

    losses = cursor.fetchone()[0]

    # ==========================================
    # WINRATE
    # ==========================================

    closed = wins + losses

    winrate = 0

    if closed > 0:

        winrate = round((wins / closed) * 100, 2)

    # ==========================================
    # PORTFOLIO
    # ==========================================

    balance = portfolio["current_balance"]

    pnl = portfolio["realized_pnl"]

    growth = (
        (balance - portfolio["starting_balance"]) / portfolio["starting_balance"]
    ) * 100

    # ==========================================
    # MESSAGE
    # ==========================================

    message = f"""
📊 VOIDMESH DAILY REPORT

📈 TOTAL TRADES:
{total_trades}

✅ WINS:
{wins}

❌ LOSSES:
{losses}

🎯 WINRATE:
{winrate}%

💰 BALANCE:
${round(balance, 2)}

📈 REALIZED PNL:
${round(pnl, 2)}

🚀 GROWTH:
{round(growth, 2)}%
"""

    # ==========================================
    # SEND TELEGRAM
    # ==========================================

    send_telegram_message(message)

    print("\nDAILY REPORT SENT")
