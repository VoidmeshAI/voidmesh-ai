# ==========================================
# FILE: backtest/reports.py
# ==========================================

from rich import print


def print_report(symbol, metrics):

    print("\n[bold green]" "BACKTEST REPORT" "[/bold green]")

    print("\n[bold cyan]" f"PAIR: {symbol}" "[/bold cyan]")

    print(f"\nTOTAL TRADES: " f"{metrics['total_trades']}")

    print(f"WINS: " f"{metrics['wins']}")

    print(f"LOSSES: " f"{metrics['losses']}")

    print(f"WINRATE: " f"{metrics['winrate']}%")

    print(f"TOTAL RR: " f"{metrics['total_rr']}R")

    # ==========================================
    # PERFORMANCE RATING
    # ==========================================

    winrate = metrics["winrate"]

    if winrate >= 70:

        rating = "ELITE"

    elif winrate >= 60:

        rating = "STRONG"

    elif winrate >= 50:

        rating = "DECENT"

    else:

        rating = "WEAK"

    print(f"\nSYSTEM RATING: " f"{rating}")

    # ==========================================
    # AI FEEDBACK
    # ==========================================

    print("\n[bold yellow]" "AI ANALYSIS:" "[/bold yellow]")

    if winrate >= 60:

        print("• Strategy shows " "strong historical performance")

    else:

        print("• Strategy requires " "further optimization")

    if metrics["total_rr"] > 0:

        print("• Positive risk-reward " "performance detected")

    else:

        print("• Negative RR performance")
