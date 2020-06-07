from typing import Optional

from gochan.models import AppContext, Thread
from gochan.event_handler import EventHandler
from gochan.client import post_response


class ResponseFormVM:
    def __init__(self, context: AppContext):
        super().__init__()
        self._app_context = context
        self._app_context.on_property_changed.add(self._app_context_changed)

        self.on_property_changed = EventHandler()

    @property
    def target(self) -> Optional[Thread]:
        return self._app_context.thread

    def post(self, name: str, mail: str, message: str) -> Optional[str]:
        # TODO: This should probably not be here and should return value
        if self._app_context.thread is not None:
            return self._app_context.thread.post(name, mail, message)

        return None

    def update_thread(self):
        if self._app_context.thread is not None:
            self._app_context.thread.update()

    def _app_context_changed(self, property_name: str):
        if property_name == "thread":
            self.on_property_changed("target")
