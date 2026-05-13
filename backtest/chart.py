# ==========================================
# FILE: backtest/chart.py
# ==========================================

import matplotlib.pyplot as plt


def plot_equity_curve(equity_curve):

    plt.figure(figsize=(12, 6))

    plt.plot(equity_curve)

    plt.title("VOIDMESH AI Equity Curve")

    plt.xlabel("Trades")

    plt.ylabel("Balance")

    plt.grid(True)

    plt.show()
