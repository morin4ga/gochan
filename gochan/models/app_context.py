from typing import TYPE_CHEKING, Callable, List, TypeVar, Generic

from gochan.event_handler import EventHandler
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Bbsmenu = None
        self.board: Board = None
        self.thread: Thread = None

        self.on_property_changed = EventHandler()

    def set_bbsmenu(self):
        self.bbsmenu = Bbsmenu.get_bbsmenu()
        self.on_property_changed("bbsmenu")

    def set_board(self, server: str, board: str):
        self.board = Board.get_board(server, board)
        self.on_property_changed("board")

    def set_thread(self, server: str, board: str, key: str):
        self.thread = Thread.get_thread(server, board, key)
        self.on_property_changed("thread")
