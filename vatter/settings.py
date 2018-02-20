import os
import sys


PROJECT_ROOT = os.path.dirname(sys.argv[0])

# Database settings
# For sqlite use: DB_PATH = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')
DB_PATH = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')


INPUT_STYLE = {
    'relief': 'flat',
    'borderwidth': 4,
    'highlightbackground': '#666666',
    'highlightthickness': 1,
}

FLOAT_FORMAT_STRING = '{0:.2f}'
