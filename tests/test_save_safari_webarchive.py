#!/usr/bin/env python3

import os
import pathlib

import pytest

from utils import save_safari_webarchive


@pytest.fixture
def out_path(tmp_path: pathlib.Path) -> None:
    """
    Returns a temporary path where we can write a webarchive.

    Any files written to this path will be cleaned up at the end of the test.
    """
    return tmp_path / "example.webarchive"


def test_creates_a_single_archive(out_path: pathlib.Path) -> None:
    result = save_safari_webarchive(["https://example.com", out_path])

    assert result["returncode"] == 0
    assert result["stdout"] is not None
    assert result["stderr"] is None
    assert out_path.exists()


def test_does_not_overwrite_existing_archive(out_path: pathlib.Path) -> None:
    out_path.write_text("This should still be here later")

    result = save_safari_webarchive(["https://example.com", out_path])

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": (
            "Unable to save webarchive file: "
            "The file “example.webarchive” couldn’t be saved in the folder "
            "“test_does_not_overwrite_existi0” because a file with "
            "the same name already exists.\n"
        ),
    }

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

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": "Usage: save_safari_webarchive.swift <URL> <OUTPUT_PATH>\n",
    }


@pytest.mark.parametrize("status_code", ["403", "404", "410", "500"])
def test_it_fails_if_non_200_status_code(
    status_code: str, out_path: pathlib.Path
) -> None:
    url = f"https://httpstat.us/{status_code}"

    result = save_safari_webarchive([url, out_path])

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": f"Failed to load {url}: got status code {status_code}\n",
    }

    assert not out_path.exists()


def test_it_fails_if_cannot_load_domain(out_path: pathlib.Path) -> None:
    result = save_safari_webarchive(["https://doesnotexist.tk/", out_path])

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": "Failed to load https://doesnotexist.tk/: A server with the specified hostname could not be found.\n",
    }

    assert not out_path.exists()


# If I run this test in GitHub Actions, I get a warning to stderr but
# the archive is saved correctly:
#
#     CFURLCopyResourcePropertyForKey failed because it was passed a URL which
#     has no scheme
#
# This test passes locally; leave it for now -- I can come back to this.
@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="This test doesn’t work correctly in GitHub Actions",
)
def test_it_fails_if_url_is_invalid(out_path: pathlib.Path) -> None:
    result = save_safari_webarchive([">", out_path])

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": "Unable to use > as a URL\n",
    }

    assert not out_path.exists()
