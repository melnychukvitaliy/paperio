'''
Entry point for all logic paperio bot. This file is using in bot.py
'''
import json

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'

# TODO: get from game object
CELLS_COUNT = 31
WIDTH = 20


def send(cmd, msg):
    'Print response message'
    return print(json.dumps({'command': cmd, 'debug': json.dumps(msg)}))


def current_player(state):
    'Returns object for current player'
    return state['params']['players']['i']


def is_in_trace(move_x, move_y, trace):
    'Define whether move is in track'

    for trace_x, trace_y in trace:
        if trace_x == move_x and trace_y == move_y:
            return True

    return False


def is_in_border(point):
    'Define whether move is in border'
    return point <= WIDTH / 2 or point >= (CELLS_COUNT * WIDTH) - WIDTH / 2


def near_territory_point(state, move_x, move_y):
    'Respond with numeric presentation how long your move from territory'
    player = current_player(state)
    near = 0

    for territory_x, territory_y in player['territory']:
        new_near = abs(territory_x - move_x) + abs(territory_y - move_y)
        if new_near < near:
            near = new_near

    return near


def score(state, from_point, to_point):
    'Numeric presentation how this way is good'
    player = current_player(state)
    moves_weight = 0.1
    if len(player['lines']) > 5:
        moves_weight = 1

    return 10 + moves_weight * moves_count(state, from_point, to_point)


def moves_count(state, from_point, to_point):
    'respond with count of moved you need to get point'
    from_x, from_y = from_point

    points_map = build_map(state, to_point)
    point_x, point_y = point_to_map(from_x, from_y)

    return points_map[point_x][point_y]


def point_to_map(point_x, point_y):
    'respond with map position for point'
    return [
        int(round((point_x - WIDTH / 2) / WIDTH)),
        int(round((point_y - WIDTH / 2) / WIDTH))
    ]


def build_map(state, to_point):
    'build a map to find right direction and calculate score'
    player = current_player(state)

    to_x, to_y = to_point
    points_map = [[None] * CELLS_COUNT for i in range(CELLS_COUNT)]

    # add obstacles
    for trace_x, trace_y in player['lines']:
        point_x, point_y = point_to_map(trace_x, trace_y)
        points_map[point_x][point_y] = 0

    # start from destination
    point_x, point_y = point_to_map(to_x, to_y)
    points_map[point_x][point_y] = 0

    # TODO add queue with points

    return build_near_map_points(points_map, point_x, point_y)


def build_near_map_points(points_map, point_x, point_y):
    'build near scores for points map. recursively call for every point '
    current_score = points_map[point_x][point_y]

    def add_next_point_score(points_map, point_x, point_y):
        'near point score calculations'
        is_available = 0 <= point_x < CELLS_COUNT and 0 <= point_y < CELLS_COUNT
        if is_available and points_map[point_x][point_y] is None:
            points_map[point_x][point_y] = current_score + 1
        return points_map

    points_map = add_next_point_score(points_map, point_x + 1, point_y)
    points_map = add_next_point_score(points_map, point_x - 1, point_y)
    points_map = add_next_point_score(points_map, point_x, point_y + 1)
    points_map = add_next_point_score(points_map, point_x, point_y - 1)

    return points_map


def y_direction(state, next_y):
    'score prediction once you are going to move forward or backward'
    player = current_player(state)
    current_x, _ = player['position']
    is_available_move = not is_in_border(next_y) and not is_in_trace(
        current_x, next_y, player['lines'])

    return score(state, [current_x, next_y], player['territory'][0]) if is_available_move else 0


def x_direction(state, next_x):
    'score prediction once you are going to move forward or backward'
    player = current_player(state)
    _, current_y = player['position']
    is_available_move = not is_in_border(next_x) and not is_in_trace(
        next_x, current_y, player['lines'])

    return score(state, [next_x, current_y], player['territory'][0]) if is_available_move else 0


def moves_min_max(state):
    '''
    Heuristics functionality to calculate score
    '''
    player = current_player(state)
    current_x, current_y = player['position']

    return {
        UP: y_direction(state, current_y + WIDTH),
        DOWN:  y_direction(state, current_y - WIDTH),
        LEFT: x_direction(state, current_x - WIDTH),
        RIGHT: x_direction(state, current_x + WIDTH)
    }


def direction(min_max_scores):
    '''
    Choose direction with max value. This is a way to move
    '''
    return max(min_max_scores, key=min_max_scores.get)


def process_tick(state):
    '''
    Define direction for each tick
    '''
    moves = moves_min_max(state)
    cmd = direction(moves)
    return send(cmd, {'position': current_player(state)['position'],
                      'cmd': cmd,
                      'moves': moves,
                      'territory': current_player(state)['territory']
                      })
