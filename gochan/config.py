import json
import re
from pathlib import Path

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from gochan.key import Key, parse_key
from gochan.widgets import Brush

KEYBINDINGS_PATH = Path(Path.home() / ".config/gochan/keybindings.json")
CACHE_PATH = Path("~/.config/gochan/cache").expanduser()
NG_PATH = Path(Path.home() / ".config/gochan/ng.json")
THEME_PATH = Path("~/.config/gochan/theme.json").expanduser()

USE_IMAGE_CACHE = True
MAX_IMAGE_CACHE = 5

USE_THREAD_CACHE = True
MAX_THREAD_CACHE = 5

BROWSER_PATH = None

conf_file = Path(Path.home() / ".config/gochan/conf.json")

if conf_file.is_file():
    conf = json.loads(conf_file.read_text())

    if "browser_path" in conf:
        BROWSER_PATH = conf["browser_path"]
    if "use_cache" in conf:
        USE_CACHE = conf["use_cache"]
    if "max_cache" in conf:
        MAX_CACHE = conf["max_cache"]
