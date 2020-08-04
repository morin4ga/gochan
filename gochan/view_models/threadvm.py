from typing import List, Optional, Union

from gochan.models import Response, AppContext
from gochan.models.ng import NG, NGResponse
from gochan.models.favorites import FavoriteThread
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs, CollectionChangedEventHandler, \
    CollectionChangedEventArgs


class ThreadVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._thread = app_context.thread
        self._filtered_responses = None
        self.on_property_changed = PropertyChangedEventHandler()
        self.on_collection_changed = CollectionChangedEventHandler()

        app_context.on_property_changed.add(self._app_context_changed)
        app_context.ng.on_collection_changed.add(self._ng_changed)
        app_context.history.on_property_changed.add(self._history_changed)
        app_context.favorites.on_property_changed.add(self._favorites_changed)

    @property
    def server(self) -> Optional[str]:
        return self._thread.server if self._thread is not None else None

    @property
    def board(self) -> Optional[str]:
        return self._thread.board if self._thread is not None else None

    @property
    def key(self) -> Optional[str]:
        return self._thread.key if self._thread is not None else None

    @property
    def title(self) -> Optional[str]:
        return self._thread.title if self._thread is not None else None

    @property
    def is_pastlog(self) -> Optional[bool]:
        return self._thread.is_pastlog if self._thread is not None else None

    @property
    def responses(self) -> Optional[List[Response]]:
        return self._thread.responses if self._thread is not None else None

    @property
    def links(self) -> Optional[List[str]]:
        return self._thread.links if self._thread is not None else None

    @property
    def bookmark(self) -> Optional[int]:
        if self._thread is not None:
            history = self._app_context.history.get(self._thread.board, self._thread.key)
            return history.bookmark if history is not None else None

    @property
    def is_favorite(self) -> Optional[bool]:
        if self._thread is not None:
            if self._thread.key in [x.key for x in self._app_context.favorites.list if isinstance(x, FavoriteThread)]:
                return True
            else:
                return False

    @property
    def filtered_responses(self) -> Optional[List[Union[NGResponse, Response]]]:
        return self._filtered_responses

    @property
    def ng(self) -> NG:
        return self._app_context.ng

    def update(self):
        if self._app_context.thread is not None:
            self._app_context.thread.update()

    def set_thread(self, server: str, board: str, key: str):
        self._app_context.set_thread(server, board, key)

    def set_image(self, url: str):
        self._app_context.set_image(url)

    def post(self, name: str, mail: str, msg: str) -> Optional[str]:
        if self._thread is not None:
            return self._thread.post(name, mail, msg)

        return None

    def add_ng_name(self, value, use_reg, hide, auto_ng_id, board, key):
        self._app_context.ng.add_ng_name(value, use_reg, hide, auto_ng_id, board, key)

    def add_ng_id(self, value, use_reg, hide, board, key):
        self._app_context.ng.add_ng_id(value, use_reg, hide, board, key)

    def add_ng_word(self, value, use_reg, hide, auto_ng_id, board, key):
        self._app_context.ng.add_ng_word(value, use_reg, hide, auto_ng_id, board, key)

    def save_history(self, bookmark: int):
        self._app_context.history.save(self._thread.board, self._thread.key, bookmark, len(self._thread.responses))

    def favorite(self):
        if self._app_context.thread is not None:
            target = self._app_context.thread

            # Check if the thread has already been registered
            for f in self._app_context.favorites.list:
                if isinstance(f, FavoriteThread) and f.key == target.key and f.board == target.board:
                    return

            self._app_context.favorites.add(FavoriteThread(
                self._app_context.thread.title, self._app_context.thread.server,
                self._app_context.thread.board, self._app_context.thread.key))

    def _app_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "thread":
            if self._thread is not None:
                self._thread.on_property_changed.remove(self._thread_property_changed)
                self._thread.on_collection_changed.remove(self._thread_collection_changed)

            self._thread = self._app_context.thread
            self._thread.on_property_changed.add(self._thread_property_changed)
            self._thread.on_collection_changed.add(self._thread_collection_changed)

            self._filtered_responses = self._app_context.ng.filter_responses(self._thread)

            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "server"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "board"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "key"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "title"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "responses"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "links"))

    def _thread_property_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "responses":
            self._filtered_responses = self._app_context.ng.filter_responses(self._thread)
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "responses"))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_responses"))

    def _thread_collection_changed(self, e: CollectionChangedEventArgs):
        if e.property_name == "responses":
            self._filtered_responses = self._app_context.ng.filter_responses(self._thread)
            self.on_collection_changed.invoke(CollectionChangedEventArgs(self, e.property_name, e.kind, e.item))
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_responses"))

    def _ng_changed(self, e: CollectionChangedEventArgs):
        if self._thread is not None:
            self._filtered_responses = self._app_context.ng.filter_responses(self._thread)
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "filtered_responses"))

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "ng"))

    def _history_changed(self, e: PropertyChangedEventArgs):
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "history"))

    def _favorites_changed(self, e: PropertyChangedEventArgs):
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_favorite"))
