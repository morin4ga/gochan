import json
import re
from pathlib import Path

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from gochan.key import Key, parse_key
from gochan.widgets import Brush

CACHE_PATH = "~/.config/gochan/cache/image"

USE_CACHE = True
MAX_CACHE = 5
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
}
KEY_BINDINGS = {
    "bbsmenu": {
        "select_up": Key.UP,
        "select_down": Key.DOWN,
        "page_up": Key.PAGE_UP,
        "page_down": Key.PAGE_DOWN,
        "select_top": Key.Ctrl.HOME,
        "select_bottom": Key.Ctrl.END,
        "select": Key.ENTER,
    },
    "board": {
        "select_up": Key.UP,
        "select_down": Key.DOWN,
        "page_up": Key.PAGE_UP,
        "page_down": Key.PAGE_DOWN,
        "select_top": Key.Ctrl.HOME,
        "select_bottom": Key.Ctrl.END,
        "select": Key.ENTER,
        "sort_1": Key.Q,
        "dsort_1": Key.Shift.Q,
        "sort_2": Key.W,
        "dsort_2": Key.Shift.W,
        "sort_3": Key.E,
        "dsort_3": Key.Shift.E,
        "sort_4": Key.R,
        "dsort_4": Key.Shift.R
    },
    "thread": {
        "open_link": Key.O,
        "scroll_up": Key.UP,
        "scroll_down": Key.DOWN,
        "page_up": Key.PAGE_UP,
        "page_down": Key.PAGE_DOWN,
        "go_to_top": Key.Ctrl.HOME,
        "go_to_bottom": Key.Ctrl.END
    }
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


keybindins_file = Path(Path.home() / ".config/gochan/keybindings.json")

if keybindins_file.is_file():
    keybindings = json.loads(keybindins_file.read_text())

    if "bbsmenu" in keybindings:
        if "select_up" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_up"] = parse_key(keybindings["bbsmenu"]["select_up"])
        if "select_down" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_down"] = parse_key(keybindings["bbsmenu"]["select_down"])
        if "page_up" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["page_up"] = parse_key(keybindings["bbsmenu"]["page_up"])
        if "page_down" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["page_down"] = parse_key(keybindings["bbsmenu"]["page_down"])
        if "select_top" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_top"] = parse_key(keybindings["bbsmenu"]["select_top"])
        if "select_bottom" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_bottom"] = parse_key(keybindings["bbsmenu"]["select_bottom"])
        if "select" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select"] = parse_key(keybindings["bbsmenu"]["select"])

    if "board" in keybindings:
        if "select_up" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_up"] = parse_key(keybindings["board"]["select_up"])
        if "select_down" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_down"] = parse_key(keybindings["board"]["select_down"])
        if "page_up" in keybindings["board"]:
            KEY_BINDINGS["board"]["page_up"] = parse_key(keybindings["board"]["page_up"])
        if "page_down" in keybindings["board"]:
            KEY_BINDINGS["board"]["page_down"] = parse_key(keybindings["board"]["page_down"])
        if "select_top" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_top"] = parse_key(keybindings["board"]["select_top"])
        if "select_bottom" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_bottom"] = parse_key(keybindings["board"]["select_bottom"])
        if "select" in keybindings["board"]:
            KEY_BINDINGS["board"]["select"] = parse_key(keybindings["board"]["select"])
        if "sort_1" in keybindings["board"]:
            KEY_BINDINGS["board"]["sort_1"] = parse_key(keybindings["board"]["sort_1"])
        if "dsort_1" in keybindings["board"]:
            KEY_BINDINGS["board"]["dsort_1"] = parse_key(keybindings["board"]["dsort_1"])
        if "sort_2" in keybindings["board"]:
            KEY_BINDINGS["board"]["sort_2"] = parse_key(keybindings["board"]["sort_2"])
        if "dsort_2" in keybindings["board"]:
            KEY_BINDINGS["board"]["dsort_2"] = parse_key(keybindings["board"]["dsort_2"])
        if "sort_3" in keybindings["board"]:
            KEY_BINDINGS["board"]["sort_3"] = parse_key(keybindings["board"]["sort_3"])
        if "dsort_3" in keybindings["board"]:
            KEY_BINDINGS["board"]["dsort_3"] = parse_key(keybindings["board"]["dsort_3"])
        if "sort_4" in keybindings["board"]:
            KEY_BINDINGS["board"]["sort_4"] = parse_key(keybindings["board"]["sort_4"])
        if "dsort_4" in keybindings["board"]:
            KEY_BINDINGS["board"]["dsort_4"] = parse_key(keybindings["board"]["dsort_4"])

    if "thread" in keybindings:
        if "open_link" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["open_link"] = parse_key(keybindings["thread"]["open_link"])
        if "scroll_up" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["scroll_up"] = parse_key(keybindings["thread"]["scroll_up"])
        if "scroll_down" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["scroll_down"] = parse_key(keybindings["thread"]["scroll_down"])
        if "page_up" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["page_up"] = parse_key(keybindings["thread"]["page_up"])
        if "page_down" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["page_down"] = parse_key(keybindings["thread"]["page_down"])
        if "go_to_top" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to_top"] = parse_key(keybindings["thread"]["go_to_top"])
        if "go_to_bottom" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to_bottom"] = parse_key(keybindings["thread"]["go_to_bottom"])
