import sys
import time as timelib
from pathlib import Path
from subprocess import DEVNULL, Popen, run
from typing import Dict, Literal, Optional, Union

File = Union[str, Path]
IntStr = Union[int, str]
Quality = Union[Literal[0], Literal[1], Literal["HIGH"], Literal["LOW"]]


def _validate_afplay():
    # Raises `FileNotFoundError` if afplay not found.
    run(["afplay"], stdout=DEVNULL, stderr=DEVNULL)


def _validate_volume(volume: IntStr) -> str:
    # Validate volume. Normally, `afplay` lets you input egregious
    # values without validation, such as negative numbers
    # which literally blew-out my laptop's speakers. Thanks Apple.
    # Anyway, here's Wonderwall.
    if isinstance(volume, str) and not volume.lstrip("-").isnumeric():
        raise ValueError("Volume must be an integer.")

    volume = int(volume)
    if volume < 0 or volume > 255:
        raise ValueError("Volume must be in range [0, 255].")

    return str(volume)


def _validate_time(time: IntStr) -> str:
    if isinstance(time, str) and not time.lstrip("-").isnumeric():
        raise ValueError("Time must be an integer.")

    if int(time) < 0:
        raise ValueError("Time must be positive.")

    return str(time)


def _validate_quality(quality: Quality) -> str:
    err_msg = "Quality must be one of [0, 1, 'HIGH', 'LOW']"
    if isinstance(quality, str):
        qual = quality.upper()
        if qual not in ("HIGH", "LOW", "0", "1"):
            raise ValueError(err_msg)

        if qual == "HIGH":
            return "1"
        elif qual == "LOW":
            return "0"

        return qual

    elif quality not in (0, 1):
        raise ValueError(err_msg)

    return str(quality)


def _validate(
    audio_file: File, volume: Optional[IntStr], time: Optional[IntStr], quality: Optional[Quality]
) -> Dict:
    _validate_afplay()

    # Validate audio file exists.
    audio_file = Path(audio_file)
    if not audio_file.is_file():
        raise FileNotFoundError(str(audio_file))

    arguments = {"audio_file": str(audio_file)}
    if volume is not None:
        arguments["volume"] = _validate_volume(volume)

    if time is not None:
        arguments["time"] = _validate_time(time)

    if quality is not None:
        arguments["quality"] = _validate_quality(quality)

    return arguments


def _main(
    audio_file: File,
    volume: Optional[IntStr],
    leaks: Optional[bool],
    time: Optional[IntStr],
    quality: Optional[Quality],
    stdout,
    stderr,
):
    arguments = _validate(audio_file, volume, time, quality)
    cmd = ["afplay", arguments["audio_file"]]
    if "volume" in arguments:
        cmd.extend(("--volume", arguments["volume"]))
    if leaks:
        cmd.append("--leaks")
    if "time" in arguments:
        cmd.extend(("--time", arguments["time"]))
    if "quality" in arguments:
        cmd.extend(("--quality", arguments["quality"]))

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
    quality: Optional[Quality] = None,
    stdout=DEVNULL,
    stderr=DEVNULL,
):
    try:
        _main(audio_file, volume, leaks, time, quality, stdout, stderr)
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
    parser.add_argument("-q", "--quality", help="Rate-scaled playback (default is 0, 1 - HIGH)")
    arguments = parser.parse_args()
    afplay(**vars(arguments))
