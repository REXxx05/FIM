from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from config import LOG_PATH, ALERT_LEVELS

console = Console()


def write_to_log(event_type, filepath, old_hash, new_hash, alert_level):
    """Write alert to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] [{alert_level}] {event_type.upper()}: {filepath}\n")
        f.write(f"  Old Hash: {old_hash}\n")
        f.write(f"  New Hash: {new_hash}\n")
        f.write(f"{'-' * 60}\n")


def print_alert(event_type, filepath, old_hash, new_hash, alert_level):
    """Print a rich formatted alert to the terminal."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pick color based on alert level
    color = "yellow" if alert_level == "WARNING" else "red"

    # Build the alert panel
    content = (
        f"[bold]Event    :[/bold] {event_type.upper()}\n"
        f"[bold]File     :[/bold] {filepath}\n"
        f"[bold]Time     :[/bold] {timestamp}\n"
        f"[bold]Old Hash :[/bold] {old_hash or 'N/A'}\n"
        f"[bold]New Hash :[/bold] {new_hash or 'N/A'}"
    )

    console.print(Panel(
        content,
        title=f"[bold {color}]⚠ {alert_level} ALERT[/bold {color}]",
        border_style=color,
        box=box.DOUBLE
    ))

    # Also write to log file
    write_to_log(event_type, filepath, old_hash, new_hash, alert_level)


def print_summary_table():
    """Print a summary table of recent events from log file."""
    console.print("\n[bold cyan]═══ FIM Event Summary ═══[/bold cyan]\n")

    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()

        if not lines:
            console.print("[yellow]No events logged yet.[/yellow]")
            return

        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED
        )
        table.add_column("Timestamp", style="cyan")
        table.add_column("Level", style="bold")
        table.add_column("Event", style="green")
        table.add_column("File", style="white")

        for line in lines:
            if line.startswith("[20"):
                parts = line.strip().split("] ")
                if len(parts) >= 3:
                    timestamp = parts[0].replace("[", "")
                    level = parts[1].replace("[", "")
                    rest = parts[2]
                    event = rest.split(":")[0]
                    filepath = rest.split(": ")[-1]

                    color = "yellow" if level == "WARNING" else "red"
                    table.add_row(
                        timestamp,
                        f"[{color}]{level}[/{color}]",
                        event,
                        filepath
                    )

        console.print(table)

    except FileNotFoundError:
        console.print("[yellow]No log file found yet.[/yellow]")


if __name__ == "__main__":
    print_summary_table()
