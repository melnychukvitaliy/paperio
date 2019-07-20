#pylint: disable=missing-docstring
from logic import is_in_border


def test_is_in_border():
    assert not is_in_border(400, 400)
