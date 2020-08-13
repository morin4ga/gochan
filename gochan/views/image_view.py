from urllib.error import HTTPError, URLError

from asciimatics.effects import Print
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.renderers import ColourImageFile
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, PopUpDialog

from gochan.event_handler import PropertyChangedEventArgs
from gochan.view_models.imagevm import ImageVM


class ImageView(Frame):
    def __init__(self, screen: Screen, data_context: ImageVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self.set_theme("user_theme")

        self._image = None

        self._data_context: ImageVM = data_context
        self._data_context.on_property_changed.add(self._context_changed)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                raise NextScene("Thread")

        return super().process_event(event)

    def _context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "image":
            if self._image is not None:
                self._scene.remove_effect(self._image)
                self._image = None

            if isinstance(self._data_context.image, HTTPError):
                err: HTTPError = self._data_context.image
                msg = str(err.code) + "\n" + err.reason
                self._scene.add_effect(PopUpDialog(self._screen, msg,
                                                   ["Close"], on_close=self._back, theme="user_theme"))
            elif isinstance(self._data_context.image, URLError):
                err: URLError = self._data_context.image
                self._scene.add_effect(PopUpDialog(self._screen, str(err.reason),
                                                   ["Close"], on_close=self._back, theme="user_theme"))
            else:
                self._image = Print(self.screen, ColourImageFile(
                    self._screen, self._data_context.image, height=self._screen.height), -1)
                self._scene.add_effect(self._image)

    def _back(self, _):
        raise NextScene("Thread")
