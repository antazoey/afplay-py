import sys
import time
from subprocess import Popen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from afplay.command import AFPlayCommand


class Player:
    """
    Play audio.
    """

    def play(self, cmd: "AFPlayCommand", stdout=sys.stdout, stderr=sys.stderr):
        popen = Popen(cmd.to_list(), stdout=stdout, stderr=stderr)

        # Wait to start playing.
        time.sleep(3)

        # Play until the end.
        while popen.poll() is None:
            time.sleep(1)
