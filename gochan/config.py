import json
from pathlib import Path

APP_DIR = Path("~/.gochan").expanduser()

KEYBINDINGS_PATH = APP_DIR / "keybindings.json"
LOG_PATH = APP_DIR / "log"
NG_PATH = APP_DIR / "ng.json"
THEME_PATH = APP_DIR / "theme.json"
HISTORY_PATH = APP_DIR / "history.json"

USE_IMAGE_CACHE = True
MAX_IMAGE_CACHE = 5

SAVE_THREAD_LOG = True
MAX_THREAD_LOG = 50

USE_BOARD_LOG = True
MAX_BOARD_LOG = 50

MAX_HISTORY = 50

NEW_THREAD_INTERVAL = 30

BROWSER_PATH = None

USER_AGENT = "Mozilla/5.0"
COOKIE = "yuki=akari"

DEFAULT_SORT = "number"

conf_file = APP_DIR / "conf.json"

if conf_file.is_file():
    conf = json.loads(conf_file.read_text())

    if "browser_path" in conf:
        BROWSER_PATH = conf["browser_path"]
    if "use_image_cache" in conf:
        USE_IMAGE_CACHE = conf["use_image_cache"]
    if "max_image_cache" in conf:
        MAX_IMAGE_CACHE = conf["max_image_cache"]
    if "save_thread_log" in conf:
        SAVE_THREAD_LOG = conf["use_thread_log"]
    if "max_thread_log" in conf:
        MAX_THREAD_LOG = conf["max_thread_log"]
    if "use_board_log" in conf:
        USE_BOARD_LOG = conf["use_board_log"]
    if "max_board_log" in conf:
        MAX_BOARD_LOG = conf["max_board_log"]
    if "user_agent" in conf:
        USER_AGENT = conf["user_agent"]
    if "cookie" in conf:
        COOKIE = conf["cookie"]
    if "default_sort" in conf:
        DEFAULT_SORT = conf["default_sort"]
    if "new_state_interval" in conf:
        NEW_THREAD_INTERVAL = conf["new_thread_interval"]
