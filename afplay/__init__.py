import sys
import time as timelib
from pathlib import Path
from subprocess import DEVNULL, Popen, run
from typing import Optional, Union

File = Union[str, Path]
IntStr = Union[int, str]


def _validate_afplay():
    # Raises `FileNotFoundError` if afplay not found.
    run(["afplay"], stdout=DEVNULL, stderr=DEVNULL)


def _validate_volume(volume: IntStr):
    # Validate volume. Normally, `afplay` lets you input egregious
    # values without validation, such as negative numbers
    # which literally blew-out my laptop's speakers. Thanks Apple.
    # Anyway, here's Wonderwall.
    if isinstance(volume, str) and not volume.lstrip("-").isnumeric():
        raise ValueError("Volume must be an integer.")

    volume = int(volume)
    if volume < 0 or volume > 255:
        raise ValueError("Volume must be in range [0, 255].")


def _validate_time(time: IntStr):
    if isinstance(time, str) and not time.lstrip("-").isnumeric():
        raise ValueError("Time must be an integer.")

    if int(time) < 0:
        raise ValueError("Time must be positive.")


def _validate(audio_file: File, volume: Optional[IntStr], time: Optional[IntStr]):
    _validate_afplay()

    # Validate audio file exists.
    audio_file = Path(audio_file)
    if not audio_file.is_file():
        raise FileNotFoundError(str(audio_file))

    if volume is not None:
        _validate_volume(volume)

    if time is not None:
        _validate_time(time)


def _main(
    audio_file: File,
    volume: Optional[IntStr],
    leaks: Optional[bool],
    time: Optional[IntStr],
    stdout,
    stderr,
):
    _validate(audio_file, volume, time)
    cmd = ["afplay", str(audio_file)]
    if volume is not None:
        cmd.extend(("--volume", str(volume)))
    if leaks is not None:
        cmd.append("--leaks")
    if time is not None:
        cmd.extend(("--time", str(time)))

    player = Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)

    # Wait to start playing.
    timelib.sleep(3)

    # Play until the end.
    while player.poll() is None:
        timelib.sleep(1)


"""Public"""


def afplay(
    audio_file: File,
    volume: Optional[IntStr] = None,
    leaks: Optional[bool] = None,
    time: Optional[IntStr] = None,
    stdout=DEVNULL,
    stderr=DEVNULL,
):
    try:
        _main(audio_file, volume, leaks, time, stdout, stderr)
    except KeyboardInterrupt:
        sys.exit(130)


def is_installed() -> bool:
    try:
        _validate_afplay()
    except FileNotFoundError:
        return False

    return True


__all__ = ["afplay"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="afplay (wrapper)", description="CLI wrapper for afplay", epilog=""
    )

    # NOTE: Must use same names as arg names from `afplay` function.
    parser.add_argument("audio_file")
    parser.add_argument("-v", "--volume", metavar="[0,255]")
    parser.add_argument("--leaks", help="Run leaks analysis", is_flag=True)
    parser.add_argument("-t", "--time", help="Time in seconds to play")
    arguments = parser.parse_args()
    afplay(**vars(arguments))
