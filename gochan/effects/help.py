from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Button, Frame, Layout
from asciimatics.screen import Screen
from gochan.widgets.richtext import Buffer, RichText, Brush
from gochan.keybinding import KEY_BINDINGS


class Help(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self.set_theme("user_theme")

        self._rich_text = RichText(screen.height - 3, Brush(
            Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD), KEY_BINDINGS["thread"])

        buf = Buffer(screen.width)

        buf.push("--Global--", Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_BOLD))
        buf.break_line(1)

        for k, v in KEY_BINDINGS["global"].items():
            buf.push("  " + k + ": ", Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.push(v.representation, Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.break_line(1)

        buf.break_line(1)
        buf.push("--Bbsmenu--", Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_BOLD))
        buf.break_line(1)

        for k, v in KEY_BINDINGS["bbsmenu"].items():
            buf.push("  " + k + ": ", Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.push(v.representation, Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.break_line(1)

        buf.break_line(1)
        buf.push("--Board--", Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_BOLD))
        buf.break_line(1)

        for k, v in KEY_BINDINGS["board"].items():
            buf.push("  " + k + ": ", Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.push(v.representation, Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.break_line(1)

        buf.break_line(1)
        buf.push("--Thread--", Brush(Screen.COLOUR_GREEN, Screen.COLOUR_BLACK, Screen.A_BOLD))
        buf.break_line(1)

        for k, v in KEY_BINDINGS["thread"].items():
            buf.push("  " + k + ": ", Brush(Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.push(v.representation, Brush(Screen.COLOUR_BLUE, Screen.COLOUR_BLACK, Screen.A_BOLD))
            buf.break_line(1)

        self._rich_text.value = buf

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(self._rich_text)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Button("Close (q)", self._on_close))

        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                self._scene.remove_effect(self)
                return None

        return super().process_event(event)

    def _on_close(self):
        self._scene.remove_effect(self)
