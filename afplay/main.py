import sys
import time as timelib
from subprocess import Popen

from afplay.arguments import CommandArguments


def main(
    arguments: CommandArguments,
    stdout=sys.stdout,
    stderr=sys.stderr,
):
    player = Popen(arguments.command, stdout=stdout, stderr=stderr)

    # Wait to start playing.
    timelib.sleep(3)

    # Play until the end.
    while player.poll() is None:
        timelib.sleep(1)
