from gochan.widgets.richtext import Brush
from gochan.keybinding import KEY_BINDINGS
from typing import Dict, List

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout

from gochan.effects.command_line import CommandLine
from gochan.models.thread import Response
from gochan.widgets.responses_viewer import ResponsesViewer


class ResponsesPopup(Frame):
    def __init__(self, screen: Screen, brushes: Dict[str, Brush], keybindings, responses: List[Response],
                 replies: Dict[int, List[Response]], ids: Dict[str, List[Response]], show_replies, show_response,
                 extract_id) -> None:
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
        self._show_replies = show_replies
        self._show_response = show_response
        self._extract_id = extract_id

        self.set_theme("user_theme")

        # Subtract 2 for the border
        self._responses_viewer = ResponsesViewer(screen.height - 2, brushes, keybindings)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._responses_viewer)

        self.fix()

        self._responses_viewer.set_data(responses, replies, ids)

    def disappear(self):
        self._scene.remove_effect(self)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["thread"]["close_popup"].value:
                self.disappear()
                return None
            elif event.key_code == KEY_BINDINGS["thread"]["show_replies"].value:
                self._scene.add_effect(CommandLine(self._screen, "show_replies:", self._show_replies))
                return None
            elif event.key_code == KEY_BINDINGS["thread"]["show_response"].value:
                self._scene.add_effect(CommandLine(self._screen, "show_response:", self._show_response))
                return None
            elif event.key_code == KEY_BINDINGS["thread"]["extract_id"].value:
                self._scene.add_effect(CommandLine(self._screen, "extract_id:", self._extract_id))
                return None

        return super().process_event(event)
