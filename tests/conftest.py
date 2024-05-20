import pathlib

import pytest


@pytest.fixture
def out_path(tmp_path: pathlib.Path) -> None:
    """
    Returns a temporary path where we can write a webarchive.

    Any files written to this path will be cleaned up at the end of the test.
    """
    return tmp_path / "example.webarchive"
