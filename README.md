# CyberSec project 

# File Integrity Monitor (FIM)

A cybersecurity tool that watches a directory for unauthorized changes,
logs every modification with timestamps, and alerts you instantly.

Built as a student project to demonstrate real-world security monitoring
concepts including cryptographic hashing, tamper-evident logging, and
real-time filesystem surveillance.

---

## Features

- Real-time file monitoring using watchdog
- SHA-256 cryptographic hashing for change detection
- HMAC signed log entries to detect log tampering
- Rich CLI alerts with color coded severity levels
- Flask web dashboard for event visualization
- SQLite database for persistent event storage
- Attack simulation script for live demonstration

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| watchdog | Filesystem event listener |
| hashlib | SHA-256 file hashing |
| hmac | Log entry signing |
| sqlite3 | Event and baseline storage |
| Flask | Web dashboard |
| Rich | Terminal UI |

---

## Project Structure

fim-project/
├── config.py          # Settings and configuration
├── database.py        # SQLite database layer
├── baseline.py        # File hashing and snapshot
├── monitor.py         # Real-time watchdog listener
├── alerts.py          # CLI alerts and HMAC signing
├── simulate_attack.py # Attack demonstration script
└── dashboard/
├── app.py         # Flask web server
└── templates/
└── index.html # Dashboard UI

---

## How It Works

1. **Baseline** — scans the watch directory and stores SHA-256
   hash, size, permissions and modification time of every file

2. **Monitor** — watchdog listens for filesystem events in real
   time. On any change, the file is rehashed and compared against
   the baseline

3. **Alert** — if hashes differ, a CRITICAL or WARNING alert fires
   in the terminal and is written to fim.log with an HMAC signature

4. **Verify** — HMAC signatures prove the log hasn't been tampered
   with after events were recorded

---

## Setup

```bash
# Clone the repo
git clone git@github.com:REXxx05/FIM.git
cd FIM

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install watchdog flask rich

# Create test directory
mkdir ~/test_directory
```

---

## Usage

```bash
# Step 1 — Take baseline snapshot
python3 baseline.py

# Step 2 — Start monitoring
python3 monitor.py

# Step 3 — Open dashboard (new terminal)
python3 dashboard/app.py
# Visit http://localhost:5000

# Step 4 — Verify log integrity
python3 alerts.py

# Step 5 — Run attack simulation
python3 simulate_attack.py
```

---

## Attack Simulation Demo

Run the included simulation to see FIM in action:

```bash
python3 simulate_attack.py
```

Simulates a real attack scenario:
- Config file modification
- Backdoor account injection
- Malware file dropped
- Backup file deleted
- Log tampering attempt — caught by HMAC verification

---

## Security Concepts Demonstrated

- **Integrity monitoring** — detecting unauthorized file changes
- **Cryptographic hashing** — SHA-256 as a file fingerprint
- **HMAC signing** — tamper evident audit trails
- **Forensic logging** — timestamped evidence chain
- **Defence in depth** — monitoring both files and the monitor itself

---

## Author

Rex 
Built on Kali Linux | July 2026
