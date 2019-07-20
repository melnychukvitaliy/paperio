# pylint: disable=missing-docstring
import pytest
from logic import is_in_border, is_in_trace


@pytest.mark.parametrize("move_x,move_y,expected", [
    (855, 15, False),
    (30, 30, False),
    (855, -15, True),
    (0, 0, True),
    (900, 900, True),
])
def test_is_in_border(move_x, move_y, expected):
    assert is_in_border(move_x, move_y) == expected


@pytest.mark.parametrize("move_x,move_y,lines,expected", [
    (855, 15, [], False),
    (230, 200, [[400, 300], [230, 300]], False),
    (855, 25, [[400, 300], [815, 0]], False),
    (855, 15, [[855, 15]], True),
    (855, 15, [[865, 15]], True),
    (855, 15, [[855, 15]], True),
    (855, 15, [[845, 0]], True),


])
def test_is_in_trace(move_x, move_y, lines, expected):
    assert is_in_trace(move_x, move_y, lines) == expected
