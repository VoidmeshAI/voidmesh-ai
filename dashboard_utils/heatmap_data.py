# ==========================================
# FILE: dashboard/heatmap_data.py
# ==========================================

from data.market_data import get_dataframe

from engines.trend_engine import get_trend
from engines.volatility_engine import get_volatility
from engines.regime_engine import detect_regime

from engines.orderflow_engine import analyze_orderflow
from engines.liquidity_engine import detect_liquidity_sweep

from ai.predictor import predict_trade_probability


def generate_heatmap():

    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

    heatmap = []

    for symbol in symbols:

        try:

            df = get_dataframe(symbol=symbol, interval="15m", limit=200)

            trend = get_trend(df)

            volatility = get_volatility(df)

            regime = detect_regime(df)

            orderflow = analyze_orderflow(df)

            liquidity = detect_liquidity_sweep(df)

            features = {
                "confidence": 70,
                "trend": trend,
                "btc_state": "STRONG_BULLISH",
                "regime": regime,
                "rr": 3,
                "rsi": 55,
                "macd": 1,
                "macd_signal": 1,
                "atr": 1,
                "ema_distance": 1,
                "volume_spike": 1,
                "orderflow_bias": 1,
                "orderflow_strength": 70,
                "liquidity_signal": 1,
                "liquidity_strength": 70,
            }

            probability = predict_trade_probability(features)

            heatmap.append(
                {
                    "Symbol": symbol,
                    "Trend": trend,
                    "Probability": probability,
                    "Orderflow": orderflow["bias"],
                    "Liquidity": liquidity["signal"],
                    "Regime": regime,
                }
            )

        except:

            pass

    return heatmap
