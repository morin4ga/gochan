from typing import Dict, List
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout
from gochan.models import Response
from gochan.widgets import ResponsesViewer, Cell


class ResponsesPopup(Frame):
    def __init__(self, screen: Screen, flush_cell: Cell, keybindings, responses: List[Response],
                 replies: Dict[int, List[Response]]) -> None:
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self._responses = responses
        self._replies = replies

        self.set_theme("user_theme")

        # Subtract 2 for the border
        self._responses_viewer = ResponsesViewer(screen.height - 2, flush_cell, keybindings)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._responses_viewer)

        self.fix()

        self._responses_viewer.set_data(responses, replies)

    def disappear(self):
        self._scene.remove_effect(self)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                self.disappear()
