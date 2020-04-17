from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from data import Bbsmenu, BoardHeader, ThreadHeader
from client import get_bbsmenu, get_board, get_thread
from views import BbsmenuView, BoardView, ThreadView

import sys


def demo(screen: Screen, scene: Scene):
    bbsmenu_view = BbsmenuView(screen, bbsmenu)
    board_view = BoardView(screen)
    thread_view = ThreadView(screen)

    current_view = None

    def open_board(hdr: BoardHeader):
        board = get_board(hdr.server, hdr.board)
        board_view.model = board
        nonlocal current_view
        current_view = board_view
        raise NextScene("Board")

    def open_thread(hdr: ThreadHeader):
        thread = get_thread(hdr.server, hdr.board, hdr.key)
        thread_view.model = thread
        nonlocal current_view
        current_view = thread_view
        raise NextScene("Thread")

    bbsmenu_view.on_board_selected = open_board
    board_view.on_thread_selected = open_thread

    def global_shortcuts(event):
        if isinstance(event, KeyboardEvent):
            if isinstance(current_view, ThreadView):
                current_view.handle_event(event)

    scenes = [
        Scene([bbsmenu_view], -1, name="Bbsmenu"),
        Scene([board_view], -1, name="Board"),
        Scene([thread_view], -1, name="Thread")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True, unhandled_input=global_shortcuts)


bbsmenu = get_bbsmenu()


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
