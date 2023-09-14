from afplay.validate import validate_afplay


def is_installed() -> bool:
    try:
        validate_afplay()
    except FileNotFoundError:
        return False

    return True
