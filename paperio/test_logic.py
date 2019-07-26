# pylint: disable=missing-docstring
import pytest
from logic import is_in_border, is_in_trace, direction


@pytest.mark.parametrize("move,expected", [
    (855, False),
    (30, False),
    (900, True),
    (915, True),
    (0, True),
])
def test_is_in_border(move, expected):
    assert is_in_border(move) == expected


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


@pytest.mark.parametrize("min_max_scores,expected", [
    ({
        'left': 10,
        'right': 10
    }, 'left'),
    ({
        'left': 10,
        'right': 11
    }, 'right'),
])
def test_direction(min_max_scores, expected):
    assert direction(min_max_scores) == expected
