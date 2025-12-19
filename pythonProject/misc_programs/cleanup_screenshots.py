import os
import time
from pathlib import Path
import logging
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).parent
LOG_RETENTION_DAYS = 30


def cleanup_old_logs():
    cutoff = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)

    for file in SCRIPT_DIR.glob("cleanup_*.log"):
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < cutoff:
                file.unlink()
                logging.info(f"Deleted old log file: {file.name}")
        except Exception as e:
            logging.exception(f"Failed to delete old log file {file}: {e}")



def cleanup_screenshots():
    # create timestamp for log file
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = SCRIPT_DIR / f"cleanup_screenshots_{timestamp}.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,  # or INFO if you want less noise
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Script cleanup_screenhots started...")

    # Set your screenshots folder path - C:\Users\lorra\OneDrive\Pictures\Screenshots
    screenshots_folder = Path.home() / "OneDrive" / "Pictures" / "Screenshots"

    if not screenshots_folder.exists():
        logging.error(f"Folder does not exist: {screenshots_folder}")
    else:
        logging.info(f"Cleaning folder: {screenshots_folder}")

    days_old = 7  # Delete files older than 7 days

    # Calculate age threshold
    now = time.time()
    age_threshold = days_old * 86400  # 86400 seconds in a day

    # Loop through files and delete old ones
    for file in screenshots_folder.glob("*.png"):
        logging.info(f"Examining the file: {file}")
        if file.is_file():
            file_age = now - file.stat().st_mtime
            if file_age > age_threshold:
                logging.info(f"Removing the file: {file}")
                try:
                    file.unlink()
                    print(f"Deleted: {file}")
                except Exception as e:
                    logging.error(f"Failed to delete {file}: {e}")
                    print(f"Failed to delete {file}: {e}")
            else:
                logging.info(f"Not removing the file (not old enough): {file}")


if __name__ == '__main__':
    cleanup_screenshots()
    cleanup_old_logs()