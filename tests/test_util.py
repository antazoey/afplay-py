from afplay.util import is_installed


def test_is_installed(mocker):
    mock = mocker.patch("afplay.util.validate_afplay")
    is_installed()
    mock.assert_called_once()
