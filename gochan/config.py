import json
from pathlib import Path

APP_DIR = Path("~/.gochan").expanduser()

KEYBINDINGS_PATH = APP_DIR / "keybindings.json"
CACHE_PATH = APP_DIR / "cache"
NG_PATH = APP_DIR / "ng.json"
THEME_PATH = APP_DIR / "theme.json"
HISTORY_PATH = APP_DIR / "history.json"
FAVORITES_PATH = APP_DIR / "favorites.json"

CACHE_IMAGE = True
MAX_IMAGE_CACHE = 5

CACHE_THREAD = True
MAX_THREAD_CACHE = 50

CACHE_BOARD = True
MAX_BOARD_CACHE = 50

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
    if "cache_image" in conf:
        CACHE_IMAGE = conf["cache_image"]
    if "max_image_cache" in conf:
        MAX_IMAGE_CACHE = conf["max_image_cache"]
    if "cache_thread" in conf:
        CACHE_THREAD = conf["cache_thread"]
    if "max_thread_cache" in conf:
        MAX_THREAD_CACHE = conf["max_thread_cache"]
    if "cache_board" in conf:
        CACHE_BOARD = conf["cache_board"]
    if "max_board_cache" in conf:
        MAX_BOARD_CACHE = conf["max_board_cache"]
    if "user_agent" in conf:
        USER_AGENT = conf["user_agent"]
    if "cookie" in conf:
        COOKIE = conf["cookie"]
    if "default_sort" in conf:
        DEFAULT_SORT = conf["default_sort"]
    if "new_state_interval" in conf:
        NEW_THREAD_INTERVAL = conf["new_thread_interval"]
