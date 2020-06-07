import sys

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import THEMES, Button, Divider, Frame, Layout, ListBox, Text, TextBox, Widget

from gochan.config import BROWSER_PATH, THEME
from gochan.key import KeyLogger
from gochan.views import BbsmenuView, BoardView, ImageView, ResponseForm, ThreadView
from gochan.models import AppContext
from gochan.view_models import BbsmenuVM, BoardVM, ThreadVM, ImageVM, ResponseFormVM


def demo(screen: Screen, scene: Scene):
    bbsmenu_view = BbsmenuView(screen)
    board_view = BoardView(screen)
    thread_view = ThreadView(screen)
    resform = ResponseForm(screen)
    image_view = ImageView(screen)
    keylog = KeyLogger(screen)

    app_context = AppContext()
    bbsmenu_view.bind(BbsmenuVM(app_context))
    board_view.bind(BoardVM(app_context))
    thread_view.bind(ThreadVM(app_context))
    image_view.bind(ImageVM(app_context))
    resform.bind(ResponseFormVM(app_context))

    app_context.set_bbsmenu()

    scenes = [
        # Scene([keylog], -1, name="Keylog"),
        Scene([bbsmenu_view], -1, name="Bbsmenu"),
        Scene([board_view], -1, name="Board"),
        Scene([thread_view], -1, name="Thread"),
        Scene([resform], -1, name="ResponseForm"),
        Scene([image_view], -1, name="ImageView")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


def main():
    # Enable user theme
    THEMES["user_theme"] = THEME

    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
