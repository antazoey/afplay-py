from pathlib import Path

from afplay import afplay

# Set to file on your computer.
EXAMPLE = Path.home() / "some_weird_animal_2.wav"
VOLUME = 2


if __name__ == "__main__":
    afplay(EXAMPLE, volume=VOLUME)
