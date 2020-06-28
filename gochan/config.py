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

USE_IMAGE_CACHE = True
MAX_IMAGE_CACHE = 5

USE_THREAD_CACHE = True
MAX_THREAD_CACHE = 5

BROWSER_PATH = None
THEME = {
    "background": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK, None, Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_BLUE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_RED),
    "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
    "control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "selected_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "focus_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "selected_focus_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_CYAN),
    "field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
}
THREAD_BRUSHES = {
    "normal": Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD),
    "name": Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_BOLD),
    "bookmark": Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_BOLD)
}

conf_file = Path(Path.home() / ".config/gochan/conf.json")

if conf_file.is_file():
    conf = json.loads(conf_file.read_text())

    if "browser_path" in conf:
        BROWSER_PATH = conf["browser_path"]
    if "use_cache" in conf:
        USE_CACHE = conf["use_cache"]
    if "max_cache" in conf:
        MAX_CACHE = conf["max_cache"]
