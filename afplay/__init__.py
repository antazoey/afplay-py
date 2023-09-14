from afplay.command import AFPlayCommand
from afplay.main import main as afplay
from afplay.util import is_installed


def cli():
    AFPlayCommand.from_sysargv().run()


__all__ = ["afplay", "is_installed"]


if __name__ == "__main__":
    cli()
