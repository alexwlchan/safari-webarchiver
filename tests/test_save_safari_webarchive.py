#!/usr/bin/env python3

import pathlib

from utils import save_safari_webarchive


def test_creates_a_single_archive(tmp_path: pathlib.Path) -> None:
    out_path = tmp_path / "example.webarchive"
    assert not out_path.exists()

    result = save_safari_webarchive(["https://example.com", str(out_path)])

    assert result["returncode"] == 0
    assert result["stdout"] is not None
    assert result["stderr"] is None
    assert out_path.exists()


def test_does_not_overwrite_existing_archive(tmp_path: pathlib.Path) -> None:
    out_path = tmp_path / "example.webarchive"
    out_path.write_text("This should still be here later")

    result = save_safari_webarchive(["https://example.com", str(out_path)])

    assert result["returncode"] == 1
    assert result["stdout"] is None
    assert result["stderr"] == (
        "Unable to save webarchive file: "
        "The file “example.webarchive” couldn’t be saved in the folder "
        "“test_does_not_overwrite_existi0” because a file with "
        "the same name already exists.\n"
    )

    assert out_path.read_text() == "This should still be here later"
