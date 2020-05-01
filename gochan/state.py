from typing import Tuple

from asciimatics.exceptions import NextScene

from gochan.client import get_bbsmenu, get_board, get_thread
from gochan.data import Bbsmenu, Board, BoardHeader, Thread, ThreadHeader


class AppState:
    def __init__(self):
        super().__init__()

        self.bbsmenu = get_bbsmenu()
        self.board: Board = None
        self.thread: Thread = None
        self.res_form: Thread = None

    def to_bbsmenu(self):
        raise NextScene("Bbsmenu")

    def open_board(self, hdr: BoardHeader):
        self.board = get_board(hdr.server, hdr.board)
        raise NextScene("Board")

    def to_board(self):
        raise NextScene("Board")

    def open_thread(self, hdr: ThreadHeader):
        self.thread = get_thread(hdr.server, hdr.board, hdr.key)
        raise NextScene("Thread")

    def to_thread(self):
        raise NextScene("Thread")

    def open_res_form(self, target: Thread):
        self.res_form = target
        raise NextScene("ResponseForm")


app_state = AppState()
