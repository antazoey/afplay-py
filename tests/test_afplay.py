import pytest

from afplay import afplay


def test_afplay(mock_main, audio_file):
    afplay(audio_file)
    mock_main.assert_called(audio_file.as_posix())


def test_afplay_file_str(mock_main, audio_file):
    afplay(audio_file.as_posix())
    mock_main.assert_called(audio_file.as_posix())


def test_afplay_missing_file(non_existing_audio_file):
    with pytest.raises(FileNotFoundError, match=str(non_existing_audio_file)):
        afplay(non_existing_audio_file)


def test_volume(mock_main, audio_file):
    afplay(audio_file, volume=5)
    mock_main.assert_called(audio_file.as_posix(), volume="5")


@pytest.mark.parametrize("value", (-5, "-5", 300, "300"))
def test_volume_out_of_range(value, audio_file):
    expected = r"Volume must be in range \[0, 255\]\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file, volume=value)


def test_volume_non_int(audio_file):
    expected = r"Volume must be an integer\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file, volume="foo")


def test_leaks(mock_main, audio_file):
    afplay(audio_file, leaks=True)
    mock_main.assert_called(audio_file.as_posix(), leaks=True)


@pytest.mark.parametrize("value", (20, "20"))
def test_time(value, mock_main, audio_file):
    afplay(audio_file, time=value)
    mock_main.assert_called(audio_file.as_posix(), time=value)


@pytest.mark.parametrize("value", (-1, "-1"))
def test_negative_time(value, audio_file):
    expected = r"Time must be positive\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file, time=value)


def test_time_non_int(audio_file):
    expected = r"Time must be an integer\."
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file, time="foo")


@pytest.mark.parametrize("value", (0, "0", "low", "LOW"))
def test_low_quality(value, mock_main, audio_file):
    afplay(audio_file, quality=value)
    mock_main.assert_called(audio_file.as_posix(), quality="0")


@pytest.mark.parametrize("value", (1, "1", "high", "HIGH"))
def test_high_quality(value, mock_main, audio_file):
    afplay(audio_file, quality=value)
    mock_main.assert_called(audio_file.as_posix(), quality="1")


@pytest.mark.parametrize("value", (20, "foo"))
def test_invalid_quality(value, audio_file):
    expected = r"Quality must be one of \[0, 1, 'HIGH', 'LOW'\]"
    with pytest.raises(ValueError, match=expected):
        afplay(audio_file, quality=value)
