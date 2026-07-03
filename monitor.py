import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import WATCH_DIRECTORY, ALERT_LEVELS
from database import get_baseline, log_event, save_baseline
from baseline import hash_file, get_file_info


class FIMEventHandler(FileSystemEventHandler):
    """Handles filesystem events detected by watchdog."""

    def __init__(self):
        self.baseline = get_baseline()
        print(f"[MONITOR] Loaded baseline with {len(self.baseline)} files.")

    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return

        filepath = event.src_path
        new_hash = hash_file(filepath)
        file_info = get_file_info(filepath)

        if not new_hash or not file_info:
            return

        old_entry = self.baseline.get(filepath)
        old_hash = old_entry["hash"] if old_entry else None

        if new_hash != old_hash:
            alert_level = ALERT_LEVELS["modified"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n[{alert_level}] MODIFIED: {filepath}")
            print(f"  Time      : {timestamp}")
            print(f"  Old Hash  : {old_hash}")
            print(f"  New Hash  : {new_hash}")

            log_event(
                event_type="modified",
                filepath=filepath,
                old_hash=old_hash,
                new_hash=new_hash,
                alert_level=alert_level
            )

            # Update baseline with new hash
            save_baseline(
                filepath=filepath,
                hash=new_hash,
                size=file_info["size"],
                modified_time=file_info["modified_time"],
                permissions=file_info["permissions"]
            )
            self.baseline[filepath] = {"hash": new_hash}

    def on_created(self, event):
        """Called when a new file is created."""
        if event.is_directory:
            return

        filepath = event.src_path
        new_hash = hash_file(filepath)
        file_info = get_file_info(filepath)

        if not new_hash or not file_info:
            return

        alert_level = ALERT_LEVELS["created"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{alert_level}] CREATED: {filepath}")
        print(f"  Time      : {timestamp}")
        print(f"  Hash      : {new_hash}")

        log_event(
            event_type="created",
            filepath=filepath,
            old_hash=None,
            new_hash=new_hash,
            alert_level=alert_level
        )

        save_baseline(
            filepath=filepath,
            hash=new_hash,
            size=file_info["size"],
            modified_time=file_info["modified_time"],
            permissions=file_info["permissions"]
        )
        self.baseline[filepath] = {"hash": new_hash}

    def on_deleted(self, event):
        """Called when a file is deleted."""
        if event.is_directory:
            return

        filepath = event.src_path
        old_entry = self.baseline.get(filepath)
        old_hash = old_entry["hash"] if old_entry else None

        alert_level = ALERT_LEVELS["deleted"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{alert_level}] DELETED: {filepath}")
        print(f"  Time      : {timestamp}")
        print(f"  Last Hash : {old_hash}")

        log_event(
            event_type="deleted",
            filepath=filepath,
            old_hash=old_hash,
            new_hash=None,
            alert_level=alert_level
        )

        if filepath in self.baseline:
            del self.baseline[filepath]


def start_monitor():
    """Start watching the directory."""
    print(f"[MONITOR] Watching: {WATCH_DIRECTORY}")
    print(f"[MONITOR] Started at: {datetime.now()}")
    print(f"[MONITOR] Press Ctrl+C to stop.\n")

    event_handler = FIMEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[MONITOR] Stopping...")
        observer.stop()

    observer.join()
    print("[MONITOR] Stopped.")


if __name__ == "__main__":
    start_monitor()
