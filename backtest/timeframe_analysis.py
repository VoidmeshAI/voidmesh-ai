# ==========================================
# FILE: backtest/timeframe_analysis.py
# ==========================================

from rich import print

from data.market_data import get_dataframe

from engines.trend_engine import get_trend
from engines.btc_filter import btc_market_filter
from engines.volatility_engine import get_volatility
from engines.regime_engine import detect_regime
from engines.probability_engine import calculate_confidence
from engines.signal_engine import generate_signal
from engines.entry_engine import generate_trade_levels

from backtest.simulator import simulate_trade
from backtest.metrics import calculate_metrics


def analyze_timeframes(symbol="BTCUSDT"):

    timeframes = ["5m", "15m", "1h"]

    print("\n[bold green]" "TIMEFRAME ANALYSIS" "[/bold green]")

    # ==========================================
    # LOOP TIMEFRAMES
    # ==========================================

    for tf in timeframes:

        results = []

        df = get_dataframe(symbol=symbol, interval=tf, limit=500)

        for i in range(100, len(df) - 20):

            current_df = df.iloc[:i]

            # ENGINES
            trend = get_trend(current_df)

            volatility = get_volatility(current_df)

            btc_state = btc_market_filter(trend, volatility)

            regime = detect_regime(current_df)

            confidence, reasons = calculate_confidence(
                trend, btc_state, volatility, regime
            )

            signal = generate_signal(trend, btc_state, confidence, True)

            if signal not in ["BUY", "SELL"]:

                continue

            trade_setup = generate_trade_levels(current_df, signal)

            if not trade_setup:

                continue

            future_df = df.iloc[i : i + 20]

            result = simulate_trade(future_df, signal, trade_setup)

            trade_data = {"result": result["result"], "rr_result": result["rr"]}

            results.append(trade_data)

        # ==========================================
        # METRICS
        # ==========================================

        metrics = calculate_metrics(results)

        print(f"\nTIMEFRAME: {tf}")

        print(f"TRADES: " f"{metrics['total_trades']}")

        print(f"WINRATE: " f"{metrics['winrate']}%")

        print(f"TOTAL RR: " f"{metrics['total_rr']}R")
