# ==========================================
# FILE: agents/battle_manager.py
# ==========================================

from rich import print

from agents.trend_agent import run_trend_agent

from agents.sniper_agent import run_sniper_agent

from agents.mean_reversion_agent import run_mean_reversion_agent


def run_agent_battle(df):

    results = {
        "TREND_AGENT": run_trend_agent(df),
        "SNIPER_AGENT": run_sniper_agent(df),
        "MEAN_REVERSION_AGENT": run_mean_reversion_agent(df),
    }

    print("\n[bold cyan]" "AI AGENT BATTLE" "[/bold cyan]")

    for agent, signal in results.items():

        print(f"{agent}: {signal}")

    return results
