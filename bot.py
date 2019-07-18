import json
import random

config = input()

while True:
    state = input()
    commands = ['left', 'right', 'up', 'down']
    cmd = random.choice(commands)
    print(json.dumps({"command": cmd, 'debug': cmd})
