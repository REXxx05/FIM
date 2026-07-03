import hmac
import hashlib
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from config import LOG_PATH, ALERT_LEVELS, HMAC_SECRET_KEY

console = Console()


def generate_hmac(message):
    """Generate HMAC signature for a log entry."""
    return hmac.new(
        HMAC_SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_log():
    """Verify all log entries have valid HMAC signatures."""
    console.print("\n[bold cyan]═══ Verifying Log Integrity ═══[/bold cyan]\n")

    try:
        with open(LOG_PATH, "r") as f:
            content = f.read()

        entries = content.strip().split("-" * 60)
        entries = [e.strip() for e in entries if e.strip()]

        all_valid = True
        for i, entry in enumerate(entries):
            lines = entry.strip().split("\n")
            hmac_line = [l for l in lines if l.startswith("HMAC:")]

            if not hmac_line:
                console.print(f"[red]⚠ Entry {i+1}: NO HMAC FOUND — possible tampering[/red]")
                all_valid = False
                continue

            stored_hmac = hmac_line[0].replace("HMAC: ", "").strip()
            message = "\n".join([l for l in lines if not l.startswith("HMAC:")])
            expected_hmac = generate_hmac(message)

            if hmac.compare_digest(stored_hmac, expected_hmac):
                console.print(f"[green]✓ Entry {i+1}: VALID[/green]")
            else:
                console.print(f"[red]✗ Entry {i+1}: INVALID — log has been tampered with[/red]")
                all_valid = False

        if all_valid:
            console.print("\n[bold green]✓ All log entries verified. Log is intact.[/bold green]")
        else:
            console.print("\n[bold red]⚠ Log integrity compromised. Investigate immediately.[/bold red]")

    except FileNotFoundError:
        console.print("[yellow]No log file found yet.[/yellow]")


def write_to_log(event_type, filepath, old_hash, new_hash, alert_level):
    """Write alert to log file with HMAC signature."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"[{timestamp}] [{alert_level}] {event_type.upper()}: {filepath}\n"
        f"  Old Hash: {old_hash}\n"
        f"  New Hash: {new_hash}"
    )

    signature = generate_hmac(message)

    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")
        f.write(f"HMAC: {signature}\n")
        f.write(f"{'-' * 60}\n")


def print_alert(event_type, filepath, old_hash, new_hash, alert_level):
    """Print a rich formatted alert to the terminal."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    color = "yellow" if alert_level == "WARNING" else "red"

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
    verify_log()
