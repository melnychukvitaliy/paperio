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


def moves_min_max(state):
    '''
    Heuristics functionality to calculate score
    '''
    player = current_player(state)
    current_x, current_y = player['position']

    def move(next_x, next_y):
        'Get direction based on borders and trace'
        is_not_border = not is_in_border(next_x, next_y)
        is_not_trace = not is_in_trace(next_x, next_y, player['lines'])
        return random.randrange(10) if is_not_border and is_not_trace else 0

    return {
        UP: move(current_x, current_y + WIDTH),
        DOWN: move(current_x, current_y - WIDTH),
        LEFT:  move(current_x - WIDTH, current_y),
        RIGHT: move(current_x + WIDTH, current_y),
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
                      'moves': moves})
