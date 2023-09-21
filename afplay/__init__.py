from afplay.cli import cli
from afplay.main import main as afplay
from afplay.util import is_installed

__all__ = ["afplay", "cli", "is_installed"]


if __name__ == "__main__":
    cli()
