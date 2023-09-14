import subprocess
import sys
from pathlib import Path

import pytest

from afplay.arguments import CommandArguments

BASE_PATH = Path(__file__).parent


@pytest.fixture(autouse=True)
def mock_main(mocker, devnull):
    class MockPlayer:
        _main = mocker.patch("afplay.main")

        def assert_called(self, *args, **kwargs):
            if not isinstance(args[0], str):
                pytest.fail(
                    "You should be expecting a `str` path, " "did you forget to call `as_posix()`?"
                )
            expected = CommandArguments(*args, **kwargs)
            self._main.assert_called_once_with(expected, stdout=sys.stdout, stderr=sys.stderr)

    return MockPlayer()


@pytest.fixture
def audio_file():
    return BASE_PATH / "foo.wav"


@pytest.fixture
def non_existing_audio_file():
    return BASE_PATH / "__NOT_EXISTS__.mp3"


@pytest.fixture
def devnull():
    return subprocess.DEVNULL
