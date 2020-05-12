from asciimatics.screen import Screen

BROWSER_PATH = r'/mnt/c/Program Files/Vivaldi/Application/vivaldi.exe'
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
