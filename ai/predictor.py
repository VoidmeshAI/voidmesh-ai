# ==========================================
# FILE: ai/predictor.py
# ==========================================

import joblib
import pandas as pd

# LOAD MODEL
model = joblib.load("ai/model.pkl")

# ==========================================
# ENCODE FEATURES
# ==========================================


def encode_features(features):

    trend_map = {"BULLISH": 1, "BEARISH": -1, "SIDEWAYS": 0}

    regime_map = {"TRENDING": 1, "RANGING": 0, "SIDEWAYS": 0}

    btc_map = {"STRONG_BULLISH": 1, "STRONG_BEARISH": -1, "NEUTRAL": 0}

    features["trend"] = trend_map.get(features["trend"], 0)

    features["btc_state"] = btc_map.get(features["btc_state"], 0)

    features["regime"] = regime_map.get(features["regime"], 0)

    return features


def predict_trade_probability(features):

    # ==========================================
    # FEATURES DF
    # ==========================================

    features = encode_features(features)

    X = pd.DataFrame(
        [
            [
                features["confidence"],
                features["trend"],
                features["btc_state"],
                features["regime"],
                features["rr"],
                features["rsi"],
                features["macd"],
                features["macd_signal"],
                features["atr"],
                features["ema_distance"],
                features["volume_spike"],
                features["orderflow_bias"],
                features["orderflow_strength"],
                features["liquidity_signal"],
                features["liquidity_strength"],
            ]
        ],
        columns=[
            "confidence",
            "trend",
            "btc_state",
            "regime",
            "rr",
            "rsi",
            "macd",
            "macd_signal",
            "atr",
            "ema_distance",
            "volume_spike",
            "orderflow_bias",
            "orderflow_strength",
            "liquidity_signal",
            "liquidity_strength",
        ],
    )

    # ==========================================
    # PREDICT
    # ==========================================

    probability = model.predict_proba(X)[0]

    # TAKE HIGHER CONFIDENCE
    probability = max(probability)

    # CONVERT TO %
    probability = probability * 100

    # SAFETY CAP
    probability = min(max(probability, 5), 95)

    return round(probability, 2)
