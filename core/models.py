from rich import print

from data.binance_client import get_klines
from engines.trend_engine import get_trend

symbol = "BTCUSDT"

# Fetch Binance candles
klines = get_klines(symbol)

# Detect trend
trend = get_trend(klines)

print(f"[bold cyan]{symbol}[/bold cyan]")
print(f"[bold green]TREND:[/bold green] {trend}")
