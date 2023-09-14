import sys
from typing import Optional, Type, Union

from afplay.command import AFPlayCommand
from afplay.player import Player
from afplay.types import File, IntStr, Quality


def main(
    audio_file: Union[File, AFPlayCommand],
    volume: Optional[IntStr] = None,
    leaks: Optional[bool] = None,
    time: Optional[IntStr] = None,
    quality: Optional[Quality] = None,
    player_cls: Type = Player,
    stdout=sys.stdout,
    stderr=sys.stderr,
):
    # note: this method is "overloaded" in a sense
    # that you can either pass in the arguments
    # and kwargs directly or the first arg can
    # just be a model already, as is the case
    # when using argparse in the cli.
    if isinstance(audio_file, AFPlayCommand):
        cmd: AFPlayCommand = audio_file

        # kwarg overrides...
        # though not really sure if someone would ever
        # pass an arguments object as the first arg
        # and then proceed to set additional kwargs after.
        if volume is not None:
            cmd.volume = volume
        if leaks is not None:
            cmd.leaks = leaks
        if time is not None:
            cmd.time = time
        if quality is not None:
            cmd.quality = quality

    else:
        cmd = AFPlayCommand.init_with_validation(
            audio_file,
            volume=volume,
            leaks=leaks,
            time=time,
            quality=quality,
            player_cls=player_cls,
        )

    try:
        cmd(stdout=stdout, stderr=stderr)
    except KeyboardInterrupt:
        sys.exit(130)
