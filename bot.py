'''
Paperio bot implementation.
'''
import json
import random

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'

BORDER = 630
WIDTH = 30


def send(cmd, msg):
    'Print response message'
    return print(json.dumps({'command': cmd, 'debug': json.dumps(msg)}))


def current_player(state):
    'Returns object for current player'
    return state['params']['players']['i']


def is_in_trace(move_x, move_y, trace):
    'Define whether move is in track'
    # TODO fix this method. isn't work in a right way
    for trace_x, trace_y in trace:
        if abs(trace_x - move_x) > 0 and abs(trace_y - move_y) > 0:
            return True

    return False


def moves_min_max(state):
    '''
    Heuristics functionality to calculate score
    '''
    player = current_player(state)
    current_x, current_y = player['position']

    def move(next_x, next_y):
        'Get direction based on borders and trace'
        is_not_border = BORDER - next_y > 0 and BORDER - next_x > 0
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
    cmd = direction(moves_min_max(state))
    return send(cmd, current_player(STATE)['lines'])


while True:
    STATE = json.loads(input())

    if STATE['type'] == 'start_game':
        send(UP, STATE['params'])

    if STATE['type'] == 'tick':
        process_tick(STATE)
