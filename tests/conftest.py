import subprocess
import sys
from pathlib import Path

import pytest

BASE_PATH = Path(__file__).parent


@pytest.fixture(autouse=True)
def mock_player(mocker, devnull):
    class MockPlayer:
        _run = mocker.patch("afplay.run")
        _popen = mocker.patch("afplay.Popen")

        def assert_played(self, _file, **kwargs):
            cmd = ["afplay", str(_file)]
            for key, val in kwargs.items():
                opt_str = f"--{key}"
                if key in ("leaks",):
                    cmd.append(opt_str)  # is_flag
                else:
                    cmd.extend((opt_str, str(val)))

            self._popen.assert_called_once_with(cmd, stdout=sys.stdout, stderr=sys.stderr)

        def assert_checked(self):
            self._run.assert_called_once_with(["afplay"], stdout=devnull, stderr=devnull)

    return MockPlayer()


@pytest.fixture
def audio_file_path():
    return BASE_PATH / "foo.wav"


@pytest.fixture(params=("path", "str"))
def audio_file(request, audio_file_path):
    if request.param == "path":
        yield audio_file_path
    else:
        yield str(audio_file_path)


@pytest.fixture
def non_existing_audio_file():
    return BASE_PATH / "__NOT_EXISTS__.mp3"


@pytest.fixture
def devnull():
    return subprocess.DEVNULL
