from asciimatics.screen import Screen


class Style:
    def __init__(self, normal: (int, int), name: (int, int)):
        super().__init__()
        self.normal = normal[0], Screen.A_BOLD, normal[1]
        self.name = name[0], Screen.A_BOLD, name[1]


style = Style(
    (Screen.COLOUR_WHITE, Screen.COLOUR_BLACK),
    (Screen.COLOUR_GREEN, Screen.COLOUR_BLACK),
)
