from typing import Callable

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget

from gochan.data import Thread
from gochan.state import app_state
from gochan.style import style
from gochan.widgets import Buffer, RichText


class ThreadView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._reload,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self._model: Thread = None

        self.palette["background"] = style.normal
        self.palette["button"] = style.normal
        self.palette["borders"] = style.normal

        self._rtext = RichText(
            Widget.FILL_FRAME,
            (" ", *style.normal),
            name="text_box",
        )

        self._back_button = Button("Back", on_click=self._back)
        self._write_button = Button("Write", on_click=self._write)

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._rtext)
        layout1.add_widget(Divider())

        layout2 = Layout([33, 33, 34])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)
        layout2.add_widget(self._write_button, 1)

        self.fix()

    def _reload(self):
        if self._model == app_state.thread:
            return

        self._model = app_state.thread
        self._rtext.reset()

        if self._model is not None:
            self._rtext.value = _convert_to_buf(self._model)
        else:
            self._rtext.value = []

    def _back(self):
        app_state.to_board()

    def _write(self):
        app_state.open_res_form(self._model)


def _convert_to_buf(thread: Thread) -> Buffer:
    buf = []

    for i, r in enumerate(thread.responses):
        meta = []

        for c in r.number:
            meta.append((c, *style.normal))

        meta.append((" ", *style.normal))

        for c in r.name:
            meta.append((c, *style.name))

        meta.append((" ", *style.normal))

        for c in r.date:
            meta.append((c, *style.normal))

        meta.append((" ", *style.normal))

        for c in r.id:
            meta.append((c, *style.normal))

        buf.append(meta)
        buf.append([])

        for l in r.message.split("\n"):
            line = []

            for c in l:
                line.append((c, *style.normal))

            buf.append(line)

        buf.append([])

    return buf
