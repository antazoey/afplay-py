import sys
import time
from pathlib import Path
from subprocess import DEVNULL, Popen, run
from typing import Union

AudioFile = Union[str, Path]


def _validate(audio_file: AudioFile):
    # Validate `afplay` command exists.
    run("afplay", stdout=DEVNULL, stderr=DEVNULL)

    # Validate audio file exists.
    audio_file = Path(audio_file)
    if not audio_file.is_file():
        raise FileNotFoundError(str(audio_file))


def _main(audio_file: AudioFile, stdout, stderr):
    _validate(audio_file)

    player = Popen(["afplay", str(audio_file)], stdout=stdout, stderr=stderr)

    # Wait to start playing.
    time.sleep(3)

    # Play until the end.
    while player.poll() is None:
        time.sleep(1)


def afplay(audio_file: AudioFile, stdout=DEVNULL, stderr=DEVNULL):
    try:
        _main(audio_file, stdout, stderr)
    except KeyboardInterrupt:
        sys.exit(130)


__all__ = ["afplay"]


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if not arguments:
        print("Missing audio file argument.")
        sys.exit(1)

    afplay(*arguments)
