import sys
import time
from pathlib import Path
from subprocess import DEVNULL, Popen, run
from typing import Optional, Union

AudioFile = Union[str, Path]
Volume = Union[int, str]


def _validate_afplay():
    # Raises `FileNotFoundError` if afplay not found.
    run("afplay", stdout=DEVNULL, stderr=DEVNULL)


def _validate_volume(volume: Volume):
    # Validate volume. Normally, `afplay` lets you input egregious
    # values without validation, such as negative numbers
    # which literally blew-out my laptop's speakers. Thanks Apple.
    # Anyway, here's Wonderwall.
    if isinstance(volume, str) and not volume.isnumeric():
        raise ValueError("Must provider integer value for volume.")

    volume = int(volume)
    if volume < 0 or volume > 255:
        raise ValueError("Volume must be in range [0, 255].")


def _validate(audio_file: AudioFile, volume: Optional[Volume]):
    _validate_afplay()

    # Validate audio file exists.
    audio_file = Path(audio_file)
    if not audio_file.is_file():
        raise FileNotFoundError(str(audio_file))

    if volume:
        _validate_volume(volume)


def _main(audio_file: AudioFile, volume: Optional[Volume], stdout, stderr):
    _validate(audio_file, volume)
    cmd = ["afplay", str(audio_file)]
    if volume:
        cmd.extend(("--volume", str(volume)))

    player = Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)

    # Wait to start playing.
    time.sleep(3)

    # Play until the end.
    while player.poll() is None:
        time.sleep(1)


"""Public"""


def afplay(
    audio_file: AudioFile,
    volume: Optional[Volume] = None,
    stdout=DEVNULL,
    stderr=DEVNULL,
):
    try:
        _main(audio_file, volume, stdout, stderr)
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
    parser.add_argument("-v", "--volume")
    arguments = parser.parse_args()
    afplay(**vars(arguments))
