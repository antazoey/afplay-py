import pytest

from afplay import afplay, is_installed


def test_afplay(mock_player, audio_file):
    afplay(audio_file)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file)


def test_volume(mock_player, audio_file_path):
    afplay(audio_file_path, volume=5)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file_path, volume=5)


def test_afplay_missing_file(non_existing_audio_file):
    with pytest.raises(FileNotFoundError, match=str(non_existing_audio_file)):
        afplay(non_existing_audio_file)


def test_is_installed(mock_player):
    is_installed()
    mock_player.assert_checked()
