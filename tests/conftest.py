import subprocess
from pathlib import Path

import pytest

BASE_PATH = Path(__file__).parent


@pytest.fixture(autouse=True)
def mock_process(mocker):
    mocker.patch("afplay.run")
    return mocker.patch("afplay.Popen")


@pytest.fixture
def audio_file():
    return BASE_PATH / "foo.wav"


@pytest.fixture
def non_existing_audio_file():
    return BASE_PATH / "__NOT_EXISTS__.mp3"


@pytest.fixture
def devnull():
    return subprocess.DEVNULL
