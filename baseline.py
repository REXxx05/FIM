import os
import hashlib
import stat
from datetime import datetime
from config import WATCH_DIRECTORY
from database import initialize_database, save_baseline


def hash_file(filepath):
    """Generate SHA-256 hash of a file's contents."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def get_file_info(filepath):
    """Get metadata about a file."""
    try:
        stats = os.stat(filepath)
        return {
            "size": stats.st_size,
            "modified_time": stats.st_mtime,
            "permissions": oct(stat.S_IMODE(stats.st_mode))
        }
    except (PermissionError, FileNotFoundError):
        return None


def create_baseline():
    """Scan watch directory and save all file hashes to database."""
    initialize_database()

    if not os.path.exists(WATCH_DIRECTORY):
        print(f"[ERROR] Watch directory does not exist: {WATCH_DIRECTORY}")
        return

    print(f"[BASELINE] Scanning: {WATCH_DIRECTORY}")
    print(f"[BASELINE] Started at: {datetime.now()}")

    count = 0
    for root, dirs, files in os.walk(WATCH_DIRECTORY):
        for filename in files:
            filepath = os.path.join(root, filename)

            file_hash = hash_file(filepath)
            file_info = get_file_info(filepath)

            if file_hash and file_info:
                save_baseline(
                    filepath=filepath,
                    hash=file_hash,
                    size=file_info["size"],
                    modified_time=file_info["modified_time"],
                    permissions=file_info["permissions"]
                )
                print(f"[+] {filepath}")
                count += 1

    print(f"[BASELINE] Complete — {count} files recorded.")


if __name__ == "__main__":
    create_baseline()
