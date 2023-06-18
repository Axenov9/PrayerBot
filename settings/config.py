import os

TOKEN = '6086808949:AAE9vyl1WKgQa_A2beWYqzf4Ct32bjkJSu0'

DB_NAME = 'priest.db'

VERSION = '0.1'

AUTHOR = 'Axenov'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join('sqlite:///' + BASE_DIR, DB_NAME)

COOLDOWN = 20*60

LEVELS = {
    1: 'NOTHING',
    2: 'CAVE',
    3: 'WOODEN',
    4: 'STONE',
    5: 'RED_STONE',
    6: 'CONCRETE'
}

COMMANDS = {
    'PRAY': 'pray',
    'START': 'start',
    'HELP': 'help',
    'ME': 'me'
}