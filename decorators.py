from functools import wraps
import re


def get_plural(value: int, plural: str, not_plural=""):
    return plural if value > 1 else not_plural


def parse_value_error(e: ValueError):
    err_message = str(e)

    match = re.search(
        r"not enough values to unpack \(expected (\d), got (\d)", err_message
    )

    if match:
        expected = int(match.group(1))
        actual = int(match.group(2))
        missing = expected - actual
        message = f"Should be {expected} argument{get_plural(expected, "s")} after the command."

        if missing < expected:
            message += f" {missing} argument{get_plural(missing, "s")} {get_plural(missing, "are", "is")} missing."

        return message

    return err_message


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return parse_value_error(e)
        except KeyError as e:
            return "Contact not found"

    return inner