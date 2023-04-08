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


@pytest.mark.parametrize("value", (-5, "-5", 300, "300"))
def test_volume_out_of_range(value, mock_player, audio_file_path):
    expected = r"Volume must be in range \[0, 255\]\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file_path, volume=value)


def test_volume_non_int(mock_player, audio_file_path):
    expected = r"Volume must be an integer\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file_path, volume="foo")


def test_leaks(mock_player, audio_file_path):
    afplay(audio_file_path, leaks=True)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file_path, leaks=True)


@pytest.mark.parametrize("value", (20, "20"))
def test_time(value, mock_player, audio_file_path):
    afplay(audio_file_path, time=value)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file_path, time=value)


@pytest.mark.parametrize("value", (-1, "-1"))
def test_negative_time(value, mock_player, audio_file_path):
    expected = r"Time must be positive\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file_path, time=value)


def test_time_non_int(mock_player, audio_file_path):
    expected = r"Time must be an integer\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file_path, time="foo")


@pytest.mark.parametrize("value", (0, "0", "low", "LOW"))
def test_low_quality(value, mock_player, audio_file_path):
    afplay(audio_file_path, quality=value)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file_path, quality="0")


@pytest.mark.parametrize("value", (1, "1", "high", "HIGH"))
def test_high_quality(value, mock_player, audio_file_path):
    afplay(audio_file_path, quality=value)
    mock_player.assert_checked()
    mock_player.assert_played(audio_file_path, quality="1")


@pytest.mark.parametrize("value", (20, "foo"))
def test_invalid_quality(value, mock_player, audio_file_path):
    expected = r"Quality must be one of \[0, 1, 'HIGH', 'LOW'\]"
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file_path, quality=value)


def test_afplay_missing_file(non_existing_audio_file):
    with pytest.raises(FileNotFoundError, match=str(non_existing_audio_file)):
        afplay(non_existing_audio_file)


def test_is_installed(mock_player):
    is_installed()
    mock_player.assert_checked()
