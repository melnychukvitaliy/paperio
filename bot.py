'''
Paperio bot implementation.
'''
import json
import random

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'


def process_tick(state):
    '''
    Define direction for each tick
    '''
    commands = [LEFT, RIGHT, UP, DOWN]
    cmd = random.choice(commands)
    return {"command": cmd, 'debug': json.dumps(state['params'])}


while True:
    STATE = json.loads(input())

    print(json.dumps({"command": UP, 'debug': STATE['type']}))

    if STATE['type'] == 'start_game':
        print(json.dumps({"command": "up"}))

    if STATE['type'] == 'tick':
        print(json.dumps(process_tick(STATE)))
