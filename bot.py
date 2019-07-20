'''
Paperio bot implementation.
'''
import json
from paperio.logic import send, process_tick, UP

while True:
    STATE = json.loads(input())

    if STATE['type'] == 'start_game':
        send(UP, STATE['params'])

    if STATE['type'] == 'tick':
        process_tick(STATE)
