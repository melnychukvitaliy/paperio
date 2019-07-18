'''
Paperio bot implementation.
'''
import json
import random

while True:
    STATE = input()
    COMMANDS = ['left', 'right', 'up', 'down']
    CMD = random.choice(COMMANDS)
    print(json.dumps({"command": CMD, 'debug': str(STATE)}))
