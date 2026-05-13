from rich import print

import database.models

from data.websocket_client import start_websocket

print("\n[bold green]" "VOIDMESH AI STARTED" "[/bold green]")

start_websocket()
