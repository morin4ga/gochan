from typing import Optional, List, Union

from gochan.models import AppContext, Thread
from gochan.models.ng import NG
from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler, CollectionChangedEventArgs


class BoardVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._board = app_context.board
        self._filtered_threads = None

        self._app_context.on_property_changed.add(self._app_context_changed)
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = PropertyChangedEventHandler()

    @property
    def board(self) -> Optional[str]:
        return self._board.board if self._board is not None else None

    @property
    def threads(self) -> Optional[List[Thread]]:
        return self._board.threads if self._board is not None else None

    @property
    def name(self) -> Optional[str]:
        return self._app_context.bbsmenu.dns[self._board.board] \
            if self._board is not None else None

    @property
    def filtered_threads(self) -> Optional[List[Union[Thread, None]]]:
        return self._filtered_threads

    @property
    def ng(self) -> NG:
        return self._app_context.ng

    def sort_threads(self, key: str, reverse=False):
        if self._board is not None:
            self._board.sort_threads(key, reverse)

    def sort_threads_by_word(self, word: str):
        if self._board is not None:
            self._board.sort_threads_by_word(word)

    def select_thread(self, idx: int):
        if self._board is not None\
                and idx < len(self._board.threads)\
                and idx >= 0:
            thread = self._board.threads[idx]
            self._app_context.set_thread(thread.server, thread.board, thread.key)

    def update(self):
        if self._board is not None:
            self._board.update()

    def add_ng_title(self, value, use_reg, board):
        self._app_context.ng.add_ng_title(value, use_reg, board)

    def _app_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "board":
            if self._board is not None:
                self._board.on_property_changed.remove(self._board_changed)

            self._board = self._app_context.board
            self._board.on_property_changed.add(self._board_changed)

            self._filtered_threads = self._app_context.ng.filter_threads(self._board)

            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_threads"))

    def _board_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "threads":
            self._filtered_threads = self._app_context.ng.filter_threads(self._board)

            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_threads"))

    def _ng_changed(self, e: CollectionChangedEventArgs):
        if self._board is not None:
            self._filtered_threads = self._app_context.ng.filter_threads(self._board)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "ng"))
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_threads"))
