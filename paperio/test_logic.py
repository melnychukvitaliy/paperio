# pylint: disable=missing-docstring
import pytest
from logic import is_in_border, is_in_trace, direction, point_to_map, moves_count


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


@pytest.mark.parametrize("point_x,point_y,expected", [
    (310, 200, [15, 10]),
    (300, 100, [14, 4]),
    (10, 10, [0, 0]),
])
def test_point_to_map(point_x, point_y, expected):
    assert point_to_map(point_x, point_y) == expected


@pytest.mark.parametrize("from_point,to_point,expected", [
    ([110, 210], [110, 190], 1),
])
def test_moves_count(from_point, to_point, expected):

    assert moves_count({
        'params': {
            'players': {
                'i': {
                    'lines': []
                }
            }
        }
    }, from_point, to_point) == expected
