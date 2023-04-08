from afplay import afplay
import pytest


def test_afplay_path(mock_process, audio_file, devnull):
    afplay(audio_file)
    mock_process.assert_called_once_with(
        ["afplay", str(audio_file)], stdout=devnull, stderr=devnull
    )


def test_afplay_str(mock_process, audio_file, devnull):
    afplay(str(audio_file))
    mock_process.assert_called_once_with(
        ["afplay", str(audio_file)], stdout=devnull, stderr=devnull
    )


def test_afplay_missing_file(non_existing_audio_file):
    with pytest.raises(FileNotFoundError, match=str(non_existing_audio_file)):
        afplay(non_existing_audio_file)
