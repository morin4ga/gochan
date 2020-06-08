from typing import Optional, Tuple

from gochan.event_handler import EventHandler
from gochan.models import AppContext


class ImageVM:
    def __init__(self, context: AppContext):
        super().__init__()
        self._app_context = context
        self._app_context.on_property_changed.add(self._context_changed)
        self.on_property_changed = EventHandler()

    @property
    def image(self) -> Optional[str]:
        return self._app_context.image

    @property
    def error(self) -> Optional[str]:
        if self._app_context.image_error is not None:
            return str(self._app_context.image_error.code) + "\n" + self._app_context.image_error.reason

    def _context_changed(self, property_name: str):
        if property_name == "image":
            self.on_property_changed("image")
        elif property_name == "image_error":
            self.on_property_changed("error")
