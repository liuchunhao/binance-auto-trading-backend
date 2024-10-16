import json
import logging

logging.basicConfig(level=logging.INFO)

def handle_socket_message(msg):
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    print(f'message: {json_str}')

# get beautiful json
def beautify_json(obj: object)->str:
    return json.dumps(obj, indent=4, sort_keys=True)

# format float to 2 decimal places
def format_float(f):
    return "{:.2f}".format(f)

def left_align(text):
    return '\n'.join([r.lstrip() for r in text.splitlines()])