from typing import Optional, List

from gochan.models import AppContext, Thread
from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler, CollectionChangedEventArgs
from gochan.config import DEFAULT_SORT


class BoardVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._board = app_context.board

        if "number" in DEFAULT_SORT:
            self._sort_by = "number"
        elif "title" in DEFAULT_SORT:
            self._sort_by = "title"
        elif "count" in DEFAULT_SORT:
            self._sort_by = "count"
        elif "speed" in DEFAULT_SORT:
            self._sort_by = "speed"

        self._reverse_sort = DEFAULT_SORT.startswith("!")

        self._active_sort = False
        self._search_word = None

        self._app_context.on_property_changed.add(self._app_context_changed)
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = PropertyChangedEventHandler()

    @property
    def board(self) -> Optional[str]:
        return self._board.board if self._board is not None else None

    @property
    def threads(self) -> Optional[List[Thread]]:
        threads = self._app_context.ng.filter_threads(self._board)

        if self._sort_by == "number":
            threads.sort(key=lambda x: x.number, reverse=self._reverse_sort)
        elif self._sort_by == "title":
            threads.sort(key=lambda x: x.title, reverse=self._reverse_sort)
        elif self._sort_by == "count":
            threads.sort(key=lambda x: x.count, reverse=self._reverse_sort)
        elif self._sort_by == "speed":
            threads.sort(key=lambda x: x.speed, reverse=self._reverse_sort)

        if self._active_sort:
            threads.sort(key=lambda x: (3 if x.count - x.bookmark > 0 else 2)
                         if x.bookmark != 0 else (1 if x.is_new else 0), reverse=True)

        if self._search_word is not None:
            threads.sort(key=lambda x: (self._search_word not in x.title))

        return threads

    @property
    def name(self) -> Optional[str]:
        return self._app_context.bbsmenu.dns[self._board.board] \
            if self._board is not None else None

    def sort_threads(self, sort_by: str, reverse_sort: bool = False):
        self._sort_by = sort_by
        self._reverse_sort = reverse_sort
        self._search_word = None
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def sort_threads_by_word(self, word: str):
        self._search_word = word
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def switch_active_sort(self):
        self._active_sort = not self._active_sort
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def set_thread(self, thread: Thread):
        self._app_context.set_thread(thread)

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

            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def _board_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "threads":
            self._search_word = None
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def _ng_changed(self, e: CollectionChangedEventArgs):
        self._search_word = None
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))
