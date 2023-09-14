import sys
from typing import Optional, Union

from afplay.arguments import CommandArguments, parse_args
from afplay.main import main
from afplay.types import File, IntStr, Quality
from afplay.util import is_installed


def afplay(
    audio_file: Union[File, CommandArguments],
    volume: Optional[IntStr] = None,
    leaks: Optional[bool] = None,
    time: Optional[IntStr] = None,
    quality: Optional[Quality] = None,
    stdout=sys.stdout,
    stderr=sys.stderr,
):
    # note: this method is "overloaded" in a sense
    # that you can either pass in the arguments
    # and kwargs directly or the first arg can
    # just be a model already, as is the case
    # when using argparse in the cli.
    if isinstance(audio_file, CommandArguments):
        arguments: CommandArguments = audio_file

        # kwarg overrides...
        # though not really sure if someone would ever
        # pass an arguments object as the first arg
        # and then proceed to set additional kwargs after.
        if volume is not None:
            arguments.volume = volume
        if leaks is not None:
            arguments.leaks = leaks
        if time is not None:
            arguments.time = time
        if quality is not None:
            arguments.quality = quality

    else:
        arguments = CommandArguments.init_with_validation(
            audio_file, volume=volume, leaks=leaks, time=time, quality=quality
        )

    try:
        main(arguments, stdout=stdout, stderr=stderr)
    except KeyboardInterrupt:
        sys.exit(130)


def cli():
    arguments = parse_args()
    afplay(arguments)


__all__ = ["afplay", "is_installed"]


if __name__ == "__main__":
    cli()
