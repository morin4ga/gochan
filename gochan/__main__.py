import sys

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene, ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import THEMES

from gochan.key import KeyLogger
from gochan.keybinding import KEY_BINDINGS
from gochan.models.app_context import AppContext
from gochan.theme import THEME
from gochan.view_models.bbsmenuvm import BbsmenuVM
from gochan.view_models.boardvm import BoardVM
from gochan.view_models.favoritesvm import FavoritesVM
from gochan.view_models.imagevm import ImageVM
from gochan.view_models.ngvm import NGVM
from gochan.view_models.threadvm import ThreadVM
from gochan.views.bbsmenu_view import BbsmenuView
from gochan.views.board_view import BoardView
from gochan.views.favorites_view import FavoritesView
from gochan.views.image_view import ImageView
from gochan.views.ng_view import NGView
from gochan.views.thread_view import ThreadView


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code

        if c == KEY_BINDINGS["global"]["exit"].value:
            raise StopApplication("stop")
        elif c == KEY_BINDINGS["global"]["bbsmenu_view"].value:
            raise NextScene("Bbsmenu")
        elif c == KEY_BINDINGS["global"]["board_view"].value:
            raise NextScene("Board")
        elif c == KEY_BINDINGS["global"]["thread_view"].value:
            raise NextScene("Thread")
        elif c == KEY_BINDINGS["global"]["ng_view"].value:
            raise NextScene("NG")
        elif c == KEY_BINDINGS["global"]["favorites_view"].value:
            raise NextScene("Favorites")


def demo(screen: Screen, scene: Scene, app_context: AppContext):
    bbsmenu_view = BbsmenuView(screen, BbsmenuVM(app_context))
    board_view = BoardView(screen, BoardVM(app_context))
    thread_view = ThreadView(screen, ThreadVM(app_context))
    image_view = ImageView(screen, ImageVM(app_context))
    ng_view = NGView(screen, NGVM(app_context))
    favorites_view = FavoritesView(screen, FavoritesVM(app_context))
    keylog = KeyLogger(screen)  # noqa: F841

    app_context.set_bbsmenu()

    scenes = [
        # Scene([keylog], -1, name="Keylog"),
        Scene([bbsmenu_view], -1, name="Bbsmenu"),
        Scene([board_view], -1, name="Board"),
        Scene([thread_view], -1, name="Thread"),
        Scene([image_view], -1, name="Image"),
        Scene([ng_view], -1, name="NG"),
        Scene([favorites_view], -1, name="Favorites")
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
            app_context.save_context()
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
