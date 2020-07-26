from typing import Optional, List

from gochan.models import AppContext, ThreadHeader
from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler, CollectionChangedEventArgs
from gochan.config import DEFAULT_SORT


class ThreadHeaderVM:
    def __init__(self, key: str, number: int, title: str, count: int, speed: int, unread: int):
        super().__init__()
        self.key = key
        self.number = number
        self.title = title
        self.count = count
        self.speed = speed
        self.unread = unread


class BoardVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._board = app_context.board
        self._threads = None

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
        self._app_context.history.on_property_changed.add(self._history_changed)
        self.on_property_changed = PropertyChangedEventHandler()

    @property
    def board(self) -> Optional[str]:
        return self._board.board if self._board is not None else None

    @property
    def threads(self) -> Optional[List[ThreadHeader]]:
        return self._threads

    @property
    def name(self) -> Optional[str]:
        return self._app_context.bbsmenu.dns[self._board.board] \
            if self._board is not None else None

    def sort_threads(self, sort_by: str, reverse_sort: bool = False):
        self._sort_by = sort_by
        self._reverse_sort = reverse_sort
        self._search_word = None
        self._update_threads()

    def sort_threads_by_word(self, word: str):
        self._search_word = word
        self._update_threads()

    def switch_active_sort(self):
        self._active_sort = not self._active_sort
        self._update_threads()

    def set_thread(self, header: ThreadHeader):
        self._app_context.set_thread(self._board.server, self._board.board, header.key)

    def update(self):
        if self._board is not None:
            self._board.update()

    def add_ng_title(self, value, use_reg, board):
        self._app_context.ng.add_ng_title(value, use_reg, board)

    def _update_threads(self):
        if self._board is None:
            return

        self._threads = []

        for t in self._app_context.ng.filter_threads(self._board.threads, self._board.board):
            history = self._app_context.history.get(self._board.board, t.key)

            if history is not None:
                unread = max(t.count, history.retrieved_reses) - history.bookmark
                self._threads.append(ThreadHeaderVM(t.key, t.number, t.title,
                                                    max(t.count, history.retrieved_reses), t.speed, unread))
            else:
                self._threads.append(ThreadHeaderVM(t.key, t.number, t.title, t.count, t.speed, None))

        if self._sort_by == "number":
            self._threads.sort(key=lambda x: x.number, reverse=self._reverse_sort)
        elif self._sort_by == "title":
            self._threads.sort(key=lambda x: x.title, reverse=self._reverse_sort)
        elif self._sort_by == "count":
            self._threads.sort(key=lambda x: x.count, reverse=self._reverse_sort)
        elif self._sort_by == "speed":
            self._threads.sort(key=lambda x: x.speed, reverse=self._reverse_sort)

        if self._active_sort:
            self._threads.sort(key=self._active_sort_key, reverse=True)

        if self._search_word is not None:
            self._threads.sort(key=lambda x: (self._search_word not in x.title))

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def _app_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "board":
            if self._board is not None:
                self._board.on_property_changed.remove(self._board_changed)

            self._board = self._app_context.board
            self._board.on_property_changed.add(self._board_changed)
            self._update_threads()

    def _board_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "threads":
            self._search_word = None
            self._update_threads()

    def _ng_changed(self, e: CollectionChangedEventArgs):
        self._search_word = None
        self._update_threads()

    def _history_changed(self, e: PropertyChangedEventArgs):
        self._update_threads()

    def _active_sort_key(self, item: ThreadHeaderVM):
        history = self._app_context.history.get(self._board.board, item.key)

        if history is None:
            return 0
        elif history.bookmark == item.count:
            return 1
        else:
            return 2
