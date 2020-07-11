import sys

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import THEMES

from gochan.keybinding import KEY_BINDINGS
from gochan.key import KeyLogger
from gochan.views import BbsmenuView, BoardView, ImageView, ThreadView, NGView
from gochan.models import AppContext
from gochan.view_models import BbsmenuVM, BoardVM, ThreadVM, ImageVM, NGVM
from gochan.theme import THEME


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code

        if c == KEY_BINDINGS["global"]["exit"]:
            raise StopApplication("stop")
        elif c == KEY_BINDINGS["global"]["bbsmenu_view"]:
            raise NextScene("Bbsmenu")
        elif c == KEY_BINDINGS["global"]["board_view"]:
            raise NextScene("Board")
        elif c == KEY_BINDINGS["global"]["thread_view"]:
            raise NextScene("Thread")
        elif c == KEY_BINDINGS["global"]["ng_view"]:
            raise NextScene("NG")


def demo(screen: Screen, scene: Scene, app_context: AppContext):
    bbsmenu_view = BbsmenuView(screen, BbsmenuVM(app_context))
    board_view = BoardView(screen, BoardVM(app_context))
    thread_view = ThreadView(screen, ThreadVM(app_context))
    image_view = ImageView(screen, ImageVM(app_context))
    ng_view = NGView(screen, NGVM(app_context))
    keylog = KeyLogger(screen)  # noqa: F841

    app_context.set_bbsmenu()

    scenes = [
        # Scene([keylog], -1, name="Keylog"),
        Scene([bbsmenu_view], -1, name="Bbsmenu"),
        Scene([board_view], -1, name="Board"),
        Scene([thread_view], -1, name="Thread"),
        Scene([image_view], -1, name="Image"),
        Scene([ng_view], -1, name="NG")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, unhandled_input=global_shortcuts, allow_int=True)


def main():
    # Enable user theme
    THEMES["user_theme"] = THEME

    app_context = AppContext()

    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene, app_context])
            app_context.save_thread()
            app_context.ng.save()
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
