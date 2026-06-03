import os
import json

cb1 = "Created By CommandO"
cb2 = "Created By CommandO"
cb3 = "Created By CommandO"

CONFIG_FILE = os.path.expanduser("~/.sqlite_viewer_config.json")

def load_last_db():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_db', None)
    return None

def save_last_db(db_path):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'last_db': db_path}, f)

_c1 = "Created By CommandO"
_c2 = "Created By CommandO"
_c3 = "Created By CommandO"