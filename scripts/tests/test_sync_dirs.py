# This file contains a set of test cases to validate the functionality of the sync_dirs.py module.
from sync_dirs import *


def test_check_directories_valid(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()

    try:
        check_directories(source, destination)
    except NotADirectoryError:
        assert False, "check_directories raised NotADirectoryError unexpectedly!"


def test_check_directories_invalid_source(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    destination.mkdir()
    try:
        check_directories(source, destination)
        assert False, "check_directories did not raise NotADirectoryError for invalid source!"
    except NotADirectoryError:
        pass


def test_check_directories_invalid_target(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()
    invalid_target = destination / "non_existent"
    try:
        check_directories(source, invalid_target)
        assert False, "check_directories did not raise NotADirectoryError for invalid target!"
    except NotADirectoryError:
        pass


def test_do_sync_file_creation(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()

    # Create a file in source directory
    src_file = source / "test_file.txt"
    src_file.write_text("This is a test file.")

    do_sync(source, destination)

    # Check if the file is created in target directory
    tgt_file = destination / "test_file.txt"
    assert tgt_file.exists(), "File was not created in target directory."
    assert tgt_file.read_text() == "This is a test file.", "File content does not match."


def test_basic_sync(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()

    # Create a test file in the source directory
    test_file = source / "example.txt"
    test_file.write_text("Hello, Lorraine!")

    # Call your sync function
    do_sync(source, destination)

    # Check that the file was copied to the destination
    synced_file = destination / "example.txt"
    assert synced_file.exists()
    assert synced_file.read_text() == "Hello, Lorraine!"


def test_do_sync_file_update(tmp_path):
    # Create source and destination directories inside tmp_path
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    destination.mkdir()

    # Create a file in source directory
    src_file = source / "update_file.txt"
    src_file.write_text("Initial content.")

    do_sync(source, destination)

    # Update the file in source directory
    src_file.write_text("Updated content.")

    do_sync(source, destination)

    # Check if the file is updated in target directory
    tgt_file = destination / "update_file.txt"
    assert tgt_file.exists(), "File was not created in target directory."
    assert tgt_file.read_text() == "Updated content.", "File content was not updated."
