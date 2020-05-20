from asciimatics.effects import Print
from asciimatics.event import KeyboardEvent
from asciimatics.renderers import ImageFile
from asciimatics.screen import Screen
from asciimatics.widgets import Frame

from gochan.controller import Controller


class ImageView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self.set_theme("user_theme")

        self._image = None
        self._file_name = None

    @property
    def image(self):
        return self._file_name

    @image.setter
    def image(self, file_name: str):
        self._file_name = file_name
        self._image = Print(self.screen, ImageFile(file_name), -1)
        self._scene.add_effect(self._image)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                if self._image is not None:
                    self._scene.remove_effect(self._image)
                    self._image = None
                    self._file_name = None

                Controller.thread.show()

        return super().process_event(event)
