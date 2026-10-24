from pathlib import Path
from convert_epub_to_pdf import resolve_folders


def test_no_arguments():
    src, tgt = resolve_folders([])
    downloads = Path.home() / "Downloads"
    assert src == downloads
    assert tgt == downloads


def test_one_argument():
    src, tgt = resolve_folders(["C:/temp"])
    assert src == Path("C:/temp")
    assert tgt == Path("C:/temp")


def test_two_arguments():
    src, tgt = resolve_folders(["C:/temp", "C:/output"])
    assert src == Path("C:/temp")
    assert tgt == Path("C:/output")


def test_too_many_arguments():
    import pytest
    with pytest.raises(ValueError):
        resolve_folders(["a", "b", "c"])
