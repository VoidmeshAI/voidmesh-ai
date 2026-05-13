# ==========================================
# FILE: ai/trainer.py
# ==========================================

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

import joblib

from ai.prepare_data import prepare_dataset


def train_model():

    # ==========================================
    # DATA
    # ==========================================

    X, y = prepare_dataset()

    # ==========================================
    # SPLIT
    # ==========================================

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ==========================================
    # MODEL
    # ==========================================

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    # ==========================================
    # TRAIN
    # ==========================================

    model.fit(X_train, y_train)

    # ==========================================
    # PREDICT
    # ==========================================

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"\nXGBOOST MODEL ACCURACY: " f"{round(accuracy * 100, 2)}%")

    # ==========================================
    # SAVE MODEL
    # ==========================================

    joblib.dump(model, "ai/model.pkl")

    print("\nMODEL SAVED:" " ai/model.pkl")
