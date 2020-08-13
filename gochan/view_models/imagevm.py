from typing import Optional, Union
from urllib.error import HTTPError, URLError

from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler
from gochan.models.app_context import AppContext


class ImageVM:
    def __init__(self, context: AppContext):
        super().__init__()
        self._app_context = context
        self._app_context.on_property_changed.add(self._context_changed)
        self.on_property_changed = PropertyChangedEventHandler()

    @property
    def image(self) -> Optional[Union[str, HTTPError, URLError]]:
        return self._app_context.image

    def _context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "image":
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "image"))
