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


# TODO add calculation
def score(state, move_x, move_y):
    'Numeric presentation how this way is good'
    return 10


def y_direction(state, next_y):
    'score prediction once you are going to move forward or backward'
    player = current_player(state)
    current_x, _ = player['position']
    is_available_move = not is_in_border(next_y) and not is_in_trace(
        current_x, next_y, player['lines'])

    return score(state, current_x, next_y) if is_available_move else 0


def x_direction(state, next_x):
    'score prediction once you are going to move forward or backward'
    player = current_player(state)
    _, current_y = player['position']
    is_available_move = not is_in_border(next_x) and not is_in_trace(
        next_x, current_y, player['lines'])

    return score(state, next_x, current_y) if is_available_move else 0


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
