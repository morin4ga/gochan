import json
import re
from pathlib import Path

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from gochan.key import Key


def get_keycode(key: str):
    m = re.search(r"ctrl-(.)", key)

    if m is not None:
        return Screen.ctrl(m.group(1))

    return ord(key)


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
THREAD_PALLET = {
    "normal": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "name": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
}
KEY_BINDINGS = {
    "thread": {
        "open_link": Key.O,
        "scroll_up": Key.UP,
        "scroll_down": Key.DOWN,
        "page_up": Key.PAGE_UP,
        "page_down": Key.PAGE_DOWN,
        "go_to_top": Key.HOME,
        "go_to_bottom": Key.END
    }
}

conf_file = Path(Path.home() / ".config/gochan/conf.json")

if conf_file.is_file():
    conf = json.loads(conf_file.read_text())

    if "browser_path" in conf:
        BROWSER_PATH = conf["browser_path"]


keybindins_file = Path(Path.home() / ".config/gochan/keybindings.json")

if keybindins_file.is_file():
    keybindings = json.loads(keybindins_file.read_text())

    if "thread" in keybindings:
        if "open_link" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["open_link"] = get_keycode(keybindings["thread"]["open_link"])
