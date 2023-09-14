import subprocess
import sys
from pathlib import Path

import pytest

from afplay.command import AFPlayCommand

BASE_PATH = Path(__file__).parent


@pytest.fixture(autouse=True)
def mock_player(mocker, devnull):
    mock = mocker.MagicMock()

    def assert_called(*args, **kwargs):
        if not isinstance(args[0], str):
            pytest.fail(
                "You should be expecting a `str` path, " "did you forget to call `as_posix()`?"
            )
        kwargs["player_cls"] = mock
        expected = AFPlayCommand(*args, **kwargs)
        mock.play.assert_called_once_with(expected, stdout=sys.stdout, stderr=sys.stderr)

    mock.assert_called = assert_called

    # Allow itself to be treated like a type, sort of.
    mock.return_value = mock
    return mock


@pytest.fixture
def audio_file():
    return BASE_PATH / "foo.wav"


@pytest.fixture
def non_existing_audio_file():
    return BASE_PATH / "__NOT_EXISTS__.mp3"


@pytest.fixture
def devnull():
    return subprocess.DEVNULL
