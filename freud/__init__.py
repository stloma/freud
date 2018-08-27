import configparser
import os
import sys
import pkg_resources

folder = 'config/'

config_file = os.path.join(folder, 'freud.ini')

__version__ = pkg_resources.get_distribution('freud').version

DEFAULT_SETTINGS = '''
[LAYOUT]
# Width of sidebar that contains server names
server_width = 15
# Height of container that holds headers
header_height = 10
# Height of container that shows server summary
summary_height = 10

[KEYS]
new_server = n
edit_server = e
send_request = r
edit_authentication = a
edit_headers = h
edit_body = b
delete_server = d
open_response_body = o
sort_servers = s
key_quick_ref = c-f

[DB]
filename = requests.db

[JSON]
indentation = 2

[SORT_BY]
# Column options: name, timestamp, url, method, body, authtype, authuser,
# authpass, headers
# Order options: asc, desc
column = timestamp
order = asc

[STYLE]
# More styles here:
# https://bitbucket.org/birkenfeld/pygments-main/src/stable/pygments/styles
theme = freud
separator_line_fg = gray
separator_line_bg = black
'''

if not os.path.exists(folder):
    os.makedirs(folder)

if not os.path.exists(config_file):
    with open(config_file, 'w') as cfile:
        cfile.write(DEFAULT_SETTINGS)

config = configparser.ConfigParser()

config.read(config_file)

if hasattr(sys, '_called_from_test'):
    config['DB']['filename'] = 'delete_freud_test_database.db'


KEYS = config['KEYS']

SERVER_WIDTH = int(config['LAYOUT']['server_width'])

HEADER_HEIGHT = int(config['LAYOUT']['header_height'])

SUMMARY_HEIGHT = int(config['LAYOUT']['summary_height'])

STYLE = config['STYLE']

DB_FILE = config['DB']['filename']

SORT_BY = config['SORT_BY']

INDENTATION = int(config['JSON']['indentation'])
