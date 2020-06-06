import re

from typing import List, Dict, Tuple

from gochan.models import Thread, Response, AppContext
from gochan.widgets import Buffer, Brush
from gochan.event_handler import EventHandler


class ThreadVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._thread = app_context.thread
        self.on_property_changed = EventHandler()

        app_context.on_property_changed.add(self._model_changed)

    @property
    def server(self):
        return self._thread.server

    @property
    def board(self):
        return self._thread.board

    @property
    def key(self):
        return self._thread.key

    @property
    def title(self):
        return self._thread.title

    @property
    def is_pastlog(self):
        return self._thread.is_pastlog

    def _app_context_changed(self, property_name: str):
        if property_name == "thread":
            pass

    def _thread_changed(self, property_name: str):
        pass
