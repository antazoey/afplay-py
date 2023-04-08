import subprocess
from pathlib import Path

import pytest

BASE_PATH = Path(__file__).parent


@pytest.fixture(autouse=True)
def mock_player(mocker, devnull):
    class MockPlayer:
        _run = mocker.patch("afplay.run")
        _popen = mocker.patch("afplay.Popen")

        def assert_played(self, _file, volume=None):
            cmd = ["afplay", str(_file)]
            if volume is not None:
                cmd.extend(("--volume", str(volume)))

            self._popen.assert_called_once_with(cmd, stdout=devnull, stderr=devnull)

        def assert_checked(self):
            return self._run.call_count > 0

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
