# ==========================================
# FILE: backtest/exporter.py
# ==========================================

import pandas as pd


def export_results(trades, filename="reports/backtest_results.csv"):

    df = pd.DataFrame(trades)

    df.to_csv(filename, index=False)

    print(f"\nRESULTS EXPORTED: " f"{filename}")
