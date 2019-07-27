# pylint: disable=missing-docstring
import pytest
from logic import is_in_border, is_in_trace, direction


@pytest.mark.parametrize("move,expected", [
    (200, False),
    (30, False),
    (610, True),
    (915, True),
    (0, True),
    (10, True),
])
def test_is_in_border(move, expected):
    assert is_in_border(move) == expected


@pytest.mark.parametrize("move_x,move_y,lines,expected", [
    (855, 15, [], False),
    (855, 25, [[25, 855]], False),
    (230, 200, [[400, 300], [230, 200]], True),
    (855, 15, [[855, 15]], True),
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
