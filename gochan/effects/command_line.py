from typing import Callable

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Text


class CommandLine(Frame):
    def __init__(self, screen: Screen, prefix: str, on_close: Callable[[str], None]):
        super().__init__(screen,
                         3,
                         int(screen.width * 0.6),
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True
                         )

        self.set_theme("user_theme")

        self._on_close = on_close

        self._text = Text(prefix)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._text)

        self.fix()

    def disappear(self):
        self._scene.remove_effect(self)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('\n'):
                self.disappear()
                self._on_close(self._text.value)
                return None

        return super().process_event(event)
