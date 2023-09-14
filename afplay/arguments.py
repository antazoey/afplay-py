import argparse
from dataclasses import dataclass
from typing import List, Optional

from afplay.types import File, IntStr, Quality
from afplay.validate import validate_path, validate_quality, validate_time, validate_volume


@dataclass
class CommandArguments:
    audio_file: File
    volume: Optional[IntStr] = None
    leaks: Optional[bool] = None
    time: Optional[IntStr] = None
    quality: Optional[Quality] = None

    @classmethod
    def init_with_validation(
        cls,
        audio_file: File,
        volume: Optional[IntStr] = None,
        leaks: Optional[bool] = None,
        time: Optional[IntStr] = None,
        quality: Optional[Quality] = None,
    ) -> "CommandArguments":
        audio_file = validate_path(audio_file)
        volume = None if volume is None else validate_volume(volume)
        time = None if time is None else validate_time(time)
        quality = None if quality is None else validate_quality(quality)
        return cls(audio_file, volume=volume, leaks=leaks, time=time, quality=quality)

    @property
    def command(self) -> List[str]:
        audio_file = (
            self.audio_file if isinstance(self.audio_file, str) else self.audio_file.as_posix()
        )
        cmd = ["afplay", audio_file]
        if self.volume is not None:
            cmd.extend(("--volume", f"{self.volume}"))
        if self.leaks:
            cmd.append("--leaks")
        if self.time is not None:
            cmd.extend(("--time", f"{self.time}"))
        if self.quality is not None:
            cmd.extend(("--quality", f"{self.quality}"))

        return cmd


def parse_args() -> CommandArguments:
    """
    Parse sys.argv.
    """

    parser = argparse.ArgumentParser(
        prog="afplay (wrapper)", description="CLI wrapper for afplay", epilog=""
    )

    # NOTE: Must use same names as arg names from `afplay` function.
    parser.add_argument("audio_file")
    parser.add_argument("-v", "--volume", metavar="[0,255]")
    parser.add_argument("--leaks", help="Run leaks analysis", action="store_true")
    parser.add_argument("-t", "--time", help="Time in seconds to play")
    parser.add_argument("-q", "--quality", help="Rate-scaled playback (default is 0, 1 - HIGH)")

    arguments = parser.parse_args()
    arg_dict = vars(arguments)
    return CommandArguments(**arg_dict)
