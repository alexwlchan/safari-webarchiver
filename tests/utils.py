import pathlib
import subprocess
import typing


class CommandOutput(typing.TypedDict):
    returncode: int
    stdout: str | None
    stderr: str | None


def save_safari_webarchive(argv: list[str | pathlib.Path]) -> CommandOutput:
    """
    Run the ``save_safari_webarchive.swift`` script and return the result.
    """
    cmd = ["swift", "save_safari_webarchive.swift"] + [str(av) for av in argv]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    if stdout is not None:
        stdout = stdout.decode("utf8")

    if stderr is not None:
        stderr = stderr.decode("utf8")

    return CommandOutput(
        returncode=proc.returncode,
        stdout=stdout or None,
        stderr=stderr or None,
    )
