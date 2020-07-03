import json
from pathlib import Path


KEYBINDINGS_PATH = Path("~/.gochan/keybindings.json").expanduser()
CACHE_PATH = Path("~/.gochan/cache").expanduser()
LOG_PATH = Path("~/.gochan/log").expanduser()
NG_PATH = Path("~/.gochan/ng.json").expanduser()
THEME_PATH = Path("~/.gochan/theme.json").expanduser()

USE_IMAGE_CACHE = True
MAX_IMAGE_CACHE = 5

SAVE_THREAD_LOG = True
MAX_THREAD_LOG = 50

BROWSER_PATH = None

USER_AGENT = "Mozilla/5.0"
COOKIE = "yuki=akari"

conf_file = Path("~/.gochan/conf.json").expanduser()

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
    if "user_agent" in conf:
        USER_AGENT = conf["user_agent"]
    if "cookie" in conf:
        COOKIE = conf["cookie"]
