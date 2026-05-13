# ==========================================
# FILE: papertrade/pnl.py
# ==========================================

from rich import print

from papertrade.portfolio import portfolio


def show_pnl():

    starting = portfolio["starting_balance"]

    current = portfolio["current_balance"]

    pnl = portfolio["realized_pnl"]

    growth = ((current - starting) / starting) * 100

    print("\n[bold green]" "PORTFOLIO STATUS" "[/bold green]")

    print(f"STARTING BALANCE: " f"${starting}")

    print(f"CURRENT BALANCE: " f"${round(current, 2)}")

    print(f"REALIZED PNL: " f"${round(pnl, 2)}")

    print(f"GROWTH: " f"{round(growth, 2)}%")
