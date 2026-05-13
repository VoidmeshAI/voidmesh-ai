# ==========================================
# FILE: backtest/regime_analysis.py
# ==========================================

from rich import print


def analyze_regimes(results):

    regimes = {}

    # ==========================================
    # GROUP BY REGIME
    # ==========================================

    for r in results:

        regime = r["regime"]

        if regime not in regimes:

            regimes[regime] = []

        regimes[regime].append(r)

    # ==========================================
    # REPORT
    # ==========================================

    print("\n[bold cyan]" "REGIME ANALYSIS" "[/bold cyan]")

    for regime, trades in regimes.items():

        total = len(trades)

        wins = 0

        total_rr = 0

        for t in trades:

            if t["result"] == "WIN":

                wins += 1

            total_rr += t["rr_result"]

        winrate = 0

        if total > 0:

            winrate = round((wins / total) * 100, 2)

        print(f"\nREGIME: {regime}")

        print(f"TRADES: {total}")

        print(f"WINRATE: {winrate}%")

        print(f"TOTAL RR: " f"{round(total_rr, 2)}R")
