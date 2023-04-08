import pytest

from afplay import afplay


def test_afplay_path(mock_player, audio_file):
    afplay(audio_file)
    mock_player.assert_played(audio_file)


def test_afplay_missing_file(non_existing_audio_file):
    with pytest.raises(FileNotFoundError, match=str(non_existing_audio_file)):
        afplay(non_existing_audio_file)
