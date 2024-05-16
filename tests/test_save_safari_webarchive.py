#!/usr/bin/env python3

import pathlib

import pytest

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


@pytest.mark.parametrize(
    "argv",
    [
        pytest.param([], id="no_arguments"),
        pytest.param(["https://example.com"], id="not_enough_arguments"),
        pytest.param(
            ["https://example.com", "example.webarchive", "--debug"],
            id="too_many_arguments",
        ),
    ],
)
def test_it_fails_if_you_supply_the_wrong_arguments(argv: list[str]) -> None:
    result = save_safari_webarchive(argv)

    assert result["returncode"] == 1
    assert result["stdout"] is None
    assert (
        result["stderr"] == "Usage: save_safari_webarchive.swift <URL> <OUTPUT_PATH>\n"
    )


@pytest.mark.parametrize("status_code", ["404", "410", "500"])
def test_it_fails_if_non_200_status_code(
    status_code: str, tmp_path: pathlib.Path
) -> None:
    out_path = tmp_path / "example.webarchive"
    assert not out_path.exists()

    url = f"https://httpstat.us/{status_code}"

    result = save_safari_webarchive([url, str(out_path)])

    assert result["returncode"] == 1
    assert result["stdout"] is None
    assert result["stderr"] == f"Failed to load {url}: got status code {status_code}\n"

    # Check a web archive wasn't created
    assert not out_path.exists()
