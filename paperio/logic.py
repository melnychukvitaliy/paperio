'''
Entry point for all logic paperio bot. This file is using in bot.py
'''
import json

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'

BORDER = 900
WIDTH = 30


def send(cmd, msg):
    'Print response message'
    return print(json.dumps({'command': cmd, 'debug': json.dumps(msg)}))


def current_player(state):
    'Returns object for current player'
    return state['params']['players']['i']


def is_in_trace(move_x, move_y, trace):
    'Define whether move is in track'

    for trace_x, trace_y in trace:
        if 0 <= abs(trace_x - move_x) < WIDTH and 0 <= abs(trace_y - move_y) < WIDTH:
            return True

    return False


def is_in_border(point):
    'Define whether move is in border'
    return point <= 0 or point >= BORDER


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


def up_direction(state):
    'score prediction once you are going to move forward'
    player = current_player(state)
    current_x, current_y = player['position']
    y_change = current_y + WIDTH

    return score(state, current_x, y_change) if not is_in_border(y_change) else 0


def left_direction(state):
    'score prediction once you are going to move left side'
    player = current_player(state)
    current_x, current_y = player['position']
    x_change = current_x - WIDTH

    return score(state, x_change, current_y) if not is_in_border(x_change) else 0


def moves_min_max(state):
    '''
    Heuristics functionality to calculate score
    '''
    return {
        UP: up_direction(state),
        DOWN:  0,  # TODO: add direction calculation
        LEFT: left_direction(state),
        RIGHT: 0  # TODO: add direction calculation
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
