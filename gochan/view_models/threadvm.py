from typing import List, Optional, Any

from gochan.models import Response, AppContext
from gochan.models.ng import NGList
from gochan.event_handler import EventHandler


class ThreadVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._thread = app_context.thread
        self.on_property_changed = EventHandler()
        self.on_collection_changed = EventHandler()

        app_context.on_property_changed.add(self._app_context_changed)
        app_context.ng.on_collection_changed.add(self._ng_changed)

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
        return self._thread.bookmark if self._thread is not None else None

    @bookmark.setter
    def bookmark(self, value):
        if self._thread is not None:
            self._thread.bookmark = value

    @property
    def ng(self) -> NGList:
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

    def _app_context_changed(self, property_name: str):
        if property_name == "thread":
            if self._thread is not None:
                self._thread.on_property_changed.remove(self._thread_changed)
                self._thread.on_collection_changed.remove(self._thread_collection_changed)

            self._thread = self._app_context.thread
            self._thread.on_property_changed.add(self._thread_changed)
            self._thread.on_collection_changed.add(self._thread_collection_changed)

            self.on_property_changed("server")
            self.on_property_changed("board")
            self.on_property_changed("key")
            self.on_property_changed("title")
            self.on_property_changed("is_pastlog")
            self.on_property_changed("responses")
            self.on_property_changed("links")

    def _thread_changed(self, property_name: str):
        if property_name == "responses":
            self.on_property_changed("responses")
        elif property_name == "bookmark":
            self.on_property_changed("bookmark")

    def _thread_collection_changed(self, property_name: str, kind: str, item: Any):
        if property_name == "responses":
            self.on_collection_changed(property_name, kind, item)

    def _ng_changed(self, property_name: str, type: str, *arg):
        self.on_property_changed("ng")
