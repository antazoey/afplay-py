from pathlib import Path
from subprocess import DEVNULL, run

from afplay.types import File, IntStr, Quality


def validate_afplay():
    # Raises `FileNotFoundError` if afplay not found.
    run(["afplay"], stdout=DEVNULL, stderr=DEVNULL)


def validate_path(path: File) -> str:
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    return path.as_posix()


def validate_volume(volume: IntStr) -> IntStr:
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


def validate_time(time: IntStr) -> IntStr:
    if isinstance(time, str) and not time.lstrip("-").isnumeric():
        raise ValueError("Time must be an integer.")

    if int(time) < 0:
        raise ValueError("Time must be positive.")

    return time


def validate_quality(quality: Quality) -> Quality:
    err_msg = (
        f"Quality must be one of " "[0, 1, 'HIGH', 'LOW'], " f"not '{quality} ({type(quality)})'."
    )
    if isinstance(quality, str):
        qual = quality.upper()
        if qual in ("1", "HIGH"):
            return "1"
        elif qual in ("0", "LOW"):
            return "0"

        raise ValueError(err_msg)

    elif quality in (0, 1):
        return f"{quality}"

    raise ValueError(err_msg)
