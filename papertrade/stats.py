# ==========================================
# FILE: papertrade/stats.py
# ==========================================

from rich import print

from papertrade.trades import active_trades


def show_stats():

    total = 0

    wins = 0

    losses = 0

    open_positions = 0

    # ==========================================
    # LOOP TRADES
    # ==========================================

    for trade in active_trades:

        total += 1

        if trade["status"] == "WIN":

            wins += 1

        elif trade["status"] == "LOSS":

            losses += 1

        elif trade["status"] == "OPEN":

            open_positions += 1

    # ==========================================
    # WINRATE
    # ==========================================

    closed = wins + losses

    winrate = 0

    if closed > 0:

        winrate = round((wins / closed) * 100, 2)

    # ==========================================
    # OUTPUT
    # ==========================================

    print("\n[bold cyan]" "PAPER TRADING STATS" "[/bold cyan]")

    print(f"TOTAL TRADES: {total}")

    print(f"WINS: {wins}")

    print(f"LOSSES: {losses}")

    print(f"OPEN TRADES: {open_positions}")

    print(f"WINRATE: {winrate}%")
