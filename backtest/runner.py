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
from backtest.reports import print_report
from backtest.exporter import export_results
from backtest.equity import build_equity_curve
from backtest.chart import plot_equity_curve
from backtest.confidence_analysis import analyze_confidence
from backtest.regime_analysis import analyze_regimes
from backtest.timeframe_analysis import analyze_timeframes
from ai.features import extract_features


def run_backtest():

    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

    results = []

    # ==========================================
    # LOOP SYMBOLS
    # ==========================================

    for symbol in symbols:

        print(f"\n[bold cyan]" f"BACKTESTING {symbol}" f"[/bold cyan]")

        df = get_dataframe(symbol=symbol, interval="15m", limit=3000)

        # ==========================================
        # LOOP CANDLES
        # ==========================================

        for i in range(100, len(df) - 20):

            current_df = df.iloc[:i]

            features = extract_features(current_df)

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

            # SAVE TRADE
            trade_data = {
                "symbol": symbol,
                "signal": signal,
                "trend": trend,
                "btc_state": btc_state,
                "volatility": volatility,
                "regime": regime,
                "confidence": confidence,
                "entry": trade_setup["entry"],
                "sl": trade_setup["sl"],
                "tp": trade_setup["tp"],
                "rr": trade_setup["rr"],
                "result": result["result"],
                "rr_result": result["rr"],
                "rsi": features["rsi"],
                "macd": features["macd"],
                "macd_signal": features["macd_signal"],
                "atr": features["atr"],
                "ema_distance": features["ema_distance"],
                "volume_spike": features["volume_spike"],
                "orderflow_bias": features["orderflow_bias"],
                "orderflow_strength": features["orderflow_strength"],
                "liquidity_signal": features["liquidity_signal"],
                "liquidity_strength": features["liquidity_strength"],
            }

            results.append(trade_data)

    # ==========================================
    # METRICS
    # ==========================================

    metrics = calculate_metrics(results)

    equity = build_equity_curve(results)

    # ==========================================
    # REPORT
    # ==========================================

    print_report("PORTFOLIO", metrics)

    print(f"\nFINAL BALANCE: " f"${equity['final_balance']}")

    print(f"MAX DRAWDOWN: " f"{equity['max_drawdown']}%")

    # ==========================================
    # EXPORT
    # ==========================================

    export_results(results)

    # ==========================================
    # CHART
    # ==========================================

    plot_equity_curve(equity["equity_curve"])

    analyze_confidence(results)

    analyze_regimes(results)

    analyze_timeframes("BTCUSDT")
