# ==========================================
# FILE: ai/retrain.py
# ==========================================

from rich import print

from ai.trainer import train_model


def retrain_ai():

    print("\n[bold cyan]" "RETRAINING AI MODEL..." "[/bold cyan]")

    # ==========================================
    # TRAIN
    # ==========================================

    train_model()

    print("\n[bold green]" "AI RETRAIN COMPLETE" "[/bold green]")
