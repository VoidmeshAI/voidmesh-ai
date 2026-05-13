# ==========================================
# FILE: backtest/confidence_analysis.py
# ==========================================

from rich import print


def analyze_confidence(results):

    buckets = {"50-60": [], "60-70": [], "70-80": [], "80-100": []}

    # ==========================================
    # SORT TRADES
    # ==========================================

    for r in results:

        confidence = r["confidence"]

        if 50 <= confidence < 60:

            buckets["50-60"].append(r)

        elif 60 <= confidence < 70:

            buckets["60-70"].append(r)

        elif 70 <= confidence < 80:

            buckets["70-80"].append(r)

        elif confidence >= 80:

            buckets["80-100"].append(r)

    # ==========================================
    # REPORT
    # ==========================================

    print("\n[bold magenta]" "CONFIDENCE ANALYSIS" "[/bold magenta]")

    for bucket, trades in buckets.items():

        total = len(trades)

        wins = 0

        for t in trades:

            if t["result"] == "WIN":

                wins += 1

        winrate = 0

        if total > 0:

            winrate = round((wins / total) * 100, 2)

        print(f"\nCONFIDENCE {bucket}")

        print(f"TRADES: {total}")

        print(f"WINRATE: {winrate}%")
