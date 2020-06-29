from typing import Optional, List

from gochan.models import AppContext, Board, ThreadHeader
from gochan.models.ng import NGList
from gochan.event_handler import EventHandler


class BoardVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._board = app_context.board

        self._app_context.on_property_changed.add(self._app_context_changed)
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = EventHandler()

    @property
    def board(self) -> Optional[str]:
        return self._board.board if self._board is not None else None

    @property
    def threads(self) -> Optional[List[ThreadHeader]]:
        return self._board.threads if self._board is not None else None

    @property
    def name(self) -> Optional[str]:
        return self._app_context.bbsmenu.dns[self._board.board] \
            if self._board is not None else None

    @property
    def ng(self) -> NGList:
        return self._app_context.ng

    def sort_thread(self, key: str, reverse=False):
        if self._board is None:
            return

        if key == "number":
            self._board.threads.sort(key=lambda x: x.number, reverse=reverse)
        elif key == "title":
            self._board.threads.sort(key=lambda x: x.title, reverse=reverse)
        elif key == "count":
            self._board.threads.sort(key=lambda x: x.count, reverse=reverse)
        elif key == "speed":
            self._board.threads.sort(key=lambda x: x.speed, reverse=reverse)

        self.on_property_changed("threads")

    def sort_thread_by_word(self, word: str):
        if self._board is not None:
            self._board.threads.sort(key=lambda x: (word not in x.title))
            self.on_property_changed("threads")

    def select_thread(self, idx: int):
        if self._board is not None\
                and idx < len(self._board.threads)\
                and idx >= 0:
            thread = self._board.threads[idx]
            self._app_context.set_thread(thread.server, thread.board, thread.key)

    def update(self):
        if self._board is not None:
            self._board.update()

    def add_ng(self, kind, value, use_reg, hide, board, key):
        self._app_context.ng.insert(kind, value, use_reg, hide, board, key)

    def _app_context_changed(self, property_name: str):
        if property_name == "board":
            if self._board is not None:
                self._board.on_property_changed.remove(self._board_changed)

            self._board = self._app_context.board
            self._board.on_property_changed.add(self._board_changed)

            self.on_property_changed("threads")

    def _board_changed(self, property_name):
        if property_name == "threads":
            self.on_property_changed("threads")

    def _ng_changed(self, property_name, kind, *args):
        self.on_property_changed("ng")
