import json

from asciimatics.screen import Screen

from gochan.config import THEME_PATH
from gochan.widgets.richtext import Brush

THEME = {
    "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK, None, Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_BLUE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_RED),
    "label": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "title": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "button": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "focus_button": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_CYAN),
    "control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "selected_control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "focus_control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "selected_focus_control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_CYAN),
    "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
    "focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_CYAN),
}

THREAD_BRUSHES = {
    "normal": Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "name": Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "bookmark": Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "number_normal": Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "number_highlight1": Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "number_highlight2": Brush(Screen.COLOUR_RED, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "id_normal": Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "id_highlight1": Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_NORMAL),
    "id_highlight2": Brush(Screen.COLOUR_RED, Screen.COLOUR_BLACK, Screen.A_NORMAL)
}


def to_intcolor(s: str) -> int:
    s = s.lower()

    if s == "black":
        return Screen.COLOUR_BLACK
    elif s == "blue":
        return Screen.COLOUR_BLUE
    elif s == "cyan":
        return Screen.COLOUR_CYAN
    elif s == "green":
        return Screen.COLOUR_GREEN
    elif s == "magenta":
        return Screen.COLOUR_MAGENTA
    elif s == "red":
        return Screen.COLOUR_RED
    elif s == "white":
        return Screen.COLOUR_WHITE
    elif s == "yellow":
        return Screen.COLOUR_YELLOW
    else:
        raise ValueError("Invalid color: " + s)


if THEME_PATH.is_file():
    theme = json.loads(THEME_PATH.read_text())

    if "ui" in theme:
        if "background" in theme["ui"]:
            fg, bg = theme["ui"]["background"]
            THEME["background"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "shadow" in theme["ui"]:
            fg, bg = theme["ui"]["shadow"]
            THEME["shadow"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "disabled" in theme["ui"]:
            fg, bg = theme["ui"]["disabled"]
            THEME["disabled"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "label" in theme["ui"]:
            fg, bg = theme["ui"]["label"]
            THEME["label"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "invalid" in theme["ui"]:
            fg, bg = theme["ui"]["invalid"]
            THEME["invalid"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "borders" in theme["ui"]:
            fg, bg = theme["ui"]["borders"]
            THEME["borders"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "scroll" in theme["ui"]:
            fg, bg = theme["ui"]["scroll"]
            THEME["scroll"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "title" in theme["ui"]:
            fg, bg = theme["ui"]["title"]
            THEME["title"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "edit_text" in theme["ui"]:
            fg, bg = theme["ui"]["edit_text"]
            THEME["edit_text"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "focus_edit_text" in theme["ui"]:
            fg, bg = theme["ui"]["focus_edit_text"]
            THEME["focus_edit_text"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "button" in theme["ui"]:
            fg, bg = theme["ui"]["button"]
            THEME["button"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "focus_button" in theme["ui"]:
            fg, bg = theme["ui"]["focus_button"]
            THEME["focus_button"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "controll" in theme["ui"]:
            fg, bg = theme["ui"]["controll"]
            THEME["controll"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "selected_controll" in theme["ui"]:
            fg, bg = theme["ui"]["selected_controll"]
            THEME["selected_controll"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "focus_controll" in theme["ui"]:
            fg, bg = theme["ui"]["focus_controll"]
            THEME["focus_controll"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "selected_focus_controll" in theme["ui"]:
            fg, bg = theme["ui"]["selected_focus_controll"]
            THEME["selected_focus_controll"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "field" in theme["ui"]:
            fg, bg = theme["ui"]["field"]
            THEME["field"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "selected_field" in theme["ui"]:
            fg, bg = theme["ui"]["selected_field"]
            THEME["selected_field"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "focus_field" in theme["ui"]:
            fg, bg = theme["ui"]["focus_field"]
            THEME["focus_field"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))
        elif "selected_focus_field" in theme["ui"]:
            fg, bg = theme["ui"]["selected_focus_field"]
            THEME["selected_focus_field"] = (to_intcolor(fg), Screen.A_NORMAL, to_intcolor(bg))

    if "thread" in theme:
        if "normal" in theme["thread"]:
            fg, bg = theme["thread"]["normal"]
            THREAD_BRUSHES["normal"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "name" in theme["thread"]:
            fg, bg = theme["thread"]["name"]
            THREAD_BRUSHES["name"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "bookmark" in theme["thread"]:
            fg, bg = theme["thread"]["bookmark"]
            THREAD_BRUSHES["bookmark"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "number_normal" in theme["thread"]:
            fg, bg = theme["thread"]["number_normal"]
            THREAD_BRUSHES["number_normal"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "number_highlight1" in theme["thread"]:
            fg, bg = theme["thread"]["number_highlight1"]
            THREAD_BRUSHES["number_highlight1"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "number_highlight2" in theme["thread"]:
            fg, bg = theme["thread"]["number_highlight2"]
            THREAD_BRUSHES["number_highlight2"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "id_normal" in theme["thread"]:
            fg, bg = theme["thread"]["id_normal"]
            THREAD_BRUSHES["id_normal"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "id_highlight1" in theme["thread"]:
            fg, bg = theme["thread"]["id_highlight1"]
            THREAD_BRUSHES["id_highlight1"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
        elif "id_highlight2" in theme["thread"]:
            fg, bg = theme["thread"]["id_highlight2"]
            THREAD_BRUSHES["id_highlight2"] = Brush(to_intcolor(fg), to_intcolor(bg), Screen.A_NORMAL)
