'''
Entry point for all logic paperio bot. This file is using in bot.py
'''
import json
import random

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


def is_in_border(move_x, move_y):
    'Define whether move is in border'
    return not (0 < move_x < BORDER and 0 < move_y < BORDER)


def near_territory_point(state, move_x, move_y):
    'Respond with numeric presentation how long your move from territory'
    player = current_player(state)
    near = 0

    for territory_x, territory_y in player['territory']:
        new_near = abs(territory_x - move_x) + abs(territory_y - move_y)
        if new_near < near:
            near = new_near

    return near


def score(state, x_change, y_change):
    'Numeric presentation how this way is good'

    player = current_player(state)
    current_x, current_y = player['position']

    next_x = current_x + x_change
    next_y = current_y + y_change
    near = near_territory_point(state, next_x, next_y)
    numeric_score = random.randrange(10)
    if near > 0:
        numeric_score = near if near < 100 else BORDER * 2 - near

    return numeric_score


def is_avaliable_move(next_x, next_y, lines):
    'Check whether point is available to move'
    is_not_border = not is_in_border(next_x, next_y)
    is_not_trace = not is_in_trace(next_x, next_y, lines)
    return is_not_border and is_not_trace


def predict_score(state, x_change, y_change):
    'Return numeric score prediction. This is using few steps based on x and y changes'
    player = current_player(state)
    current_x, current_y = player['position']

    def level_move(level):
        'Multiply changes for particular layer'
        return is_avaliable_move(
            current_x + x_change * level, current_y + y_change * level, player['lines'])

    return score(state, x_change, y_change) if level_move(1) and level_move(2) else 0


def moves_min_max(state):
    '''
    Heuristics functionality to calculate score
    '''
    return {
        UP: predict_score(state, 0, WIDTH),
        DOWN:  predict_score(state, 0, -WIDTH),
        LEFT: predict_score(state, -WIDTH, 0),
        RIGHT: predict_score(state, WIDTH, 0)
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
                      'moves': moves,
                      'territory': current_player(state)['territory']
                      })
