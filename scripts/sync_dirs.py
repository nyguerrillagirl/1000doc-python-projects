# This script is used to copy over new files from arg1 to arg2 where
# arg1 is the sourceDirectory and arg2 is the targetDirectory
# both parameters are added for new or updated files.
# Note: This is to be invoked as part of a script that runs twice a week Monday and Thursday

import sys
from pathlib import Path
import logging


def fetch_arguments():
    if len(sys.argv) != 3:
        raise ValueError("Expected exactly 2 arguments: <arg1> <arg2>")
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    return arg1, arg2


def setup_logger(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def log_and_raise(exc_type, message):
    logging.error(message)
    raise exc_type(message)


def check_directories(source_dir, target_dir):
    source_is_dir = Path(source_dir).is_dir()
    target_is_dir = Path(target_dir).is_dir()
    if not source_is_dir or not target_is_dir:
        raise NotADirectoryError(f"Source directory '{source_dir}' is not a valid directory or Target directory '{target_dir}' is not a valid directory.")


def do_sync(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # iterate through all files and directories in source_path
    for item in source_path.rglob('*'):
        # construct relative path with respect to source_path
        relative_path = item.relative_to(source_path)
        # actual name of file or directory we want to make sure is "in sync" in target_path
        target_item = target_path / relative_path

        if item.is_dir():
            # create the directory in target "if missing"
            if not target_item.exists():
                logging.info(f"Creating directory: {target_item}")
            target_item.mkdir(parents=True, exist_ok=True)
        else:
            # skip checking the file sync_log.txt
            if item.name == "sync_log.txt":
                continue
            # sync file if and only if it has been updated or is missing
            if not target_item.exists():
                logging.info(f"Creating file: {target_item}")
            elif item.stat().st_mtime > target_item.stat().st_mtime:
                logging.info(f"Updating file: {target_item}")

            if not target_item.exists() or item.stat().st_mtime > target_item.stat().st_mtime:
                target_item.parent.mkdir(parents=True, exist_ok=True)
                with item.open('rb') as src_file, target_item.open('wb') as dst_file:
                    dst_file.write(src_file.read())


def main():
    # obtain source and target directories
    source_dir, target_dir = fetch_arguments()
    # Create log file
    log_file = source_dir + "\\sync_log.txt"
    setup_logger(log_file)

    # check that the directories exist
    check_directories(source_dir, target_dir)

    # Create log file in source_dir to record all sync activities

    do_sync(source_dir, target_dir)

    print("main completed")


if __name__ == "__main__":
    main()
