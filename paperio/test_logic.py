# pylint: disable=missing-docstring
import pytest
from logic import is_in_border


@pytest.mark.parametrize("move_x,move_y,expected", [
    (855, 15, False),
    (855, -15, True),
    (0, 0, True),
    (900, 900, True),
])
def test_is_in_border(move_x, move_y, expected):
    assert is_in_border(move_x, move_y) == expected
