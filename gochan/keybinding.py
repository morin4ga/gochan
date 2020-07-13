import json

from gochan.config import KEYBINDINGS_PATH
from gochan.key import parse_key, Key

KEY_BINDINGS = {
    "global": {
        "exit": Key.Ctrl.C,
        "bbsmenu_view": Key.Ctrl.H,
        "board_view": Key.Ctrl.J,
        "thread_view": Key.Ctrl.K,
        "ng_view": Key.Ctrl.L
    },
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
        "dsort_4": Key.Shift.R,
        "find": Key.F,
        "ng_title": Key.N,
        "update": Key.U,
        "back": Key.B
    },
    "thread": {
        "scroll_up": Key.UP,
        "scroll_down": Key.DOWN,
        "page_up": Key.PAGE_UP,
        "page_down": Key.PAGE_DOWN,
        "go_to_top": Key.Ctrl.HOME,
        "go_to_bottom": Key.Ctrl.END,
        "open_link": Key.O,
        "show_image": Key.S,
        "go_to": Key.G,
        "ng_name": Key.N,
        "ng_id": Key.I,
        "ng_word": Key.W,
        "update": Key.U,
        "back": Key.B
    },
    "ng": {
        "delete": Key.D,
        "edit": Key.E
    }
}

if KEYBINDINGS_PATH.is_file():
    keybindings = json.loads(KEYBINDINGS_PATH.read_text())

    if "global" in keybindings:
        if "exit" in keybindings["global"]:
            KEY_BINDINGS["global"]["exit"] = parse_key(keybindings["global"]["exit"])
        if "bbsmenu_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["bbsmenu_view"] = parse_key(keybindings["global"]["bbsmenu_view"])
        if "board_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["board_view"] = parse_key(keybindings["global"]["board_view"])
        if "thread_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["thread_view"] = parse_key(keybindings["global"]["thread_view"])
        if "ng_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["ng_view"] = parse_key(keybindings["global"]["ng_view"])

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
        if "find" in keybindings["board"]:
            KEY_BINDINGS["board"]["find"] = parse_key(keybindings["board"]["find"])
        if "ng_title" in keybindings["board"]:
            KEY_BINDINGS["board"]["ng_title"] = parse_key(keybindings["board"]["ng_title"])
        if "update" in keybindings["board"]:
            KEY_BINDINGS["board"]["update"] = parse_key(keybindings["board"]["update"])
        if "back" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["back"] = parse_key(keybindings["thread"]["back"])

    if "thread" in keybindings:
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
        if "open_link" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["open_link"] = parse_key(keybindings["thread"]["open_link"])
        if "show_image" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["show_image"] = parse_key(keybindings["thread"]["show_image"])
        if "go_to" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to"] = parse_key(keybindings["thread"]["go_to"])
        if "ng_name" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_name"] = parse_key(keybindings["thread"]["ng_name"])
        if "ng_id" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_id"] = parse_key(keybindings["thread"]["ng_id"])
        if "ng_word" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_word"] = parse_key(keybindings["thread"]["ng_word"])
        if "update" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["updete"] = parse_key(keybindings["thread"]["update"])
        if "back" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["back"] = parse_key(keybindings["thread"]["back"])
