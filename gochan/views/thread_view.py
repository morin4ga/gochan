import re
from typing import Callable

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget

from gochan.browser import open_link, open_links
from gochan.config import BROWSER_PATH, KEY_BINDINGS, THREAD_PALLET
from gochan.data import Thread
from gochan.effects import CommandLine
from gochan.controller import Controller
from gochan.widgets import Buffer, RichText


class ThreadView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self._model: Thread = None

        self._inputing_cmd: bool = False

        self.set_theme("user_theme")

        self._rtext = RichText(
            Widget.FILL_FRAME,
            (" ", *THREAD_PALLET["normal"]),
            KEY_BINDINGS["thread"],
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

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Thread):
        self._model = model
        self._update_buffer()
        self._rtext.reset_offset()

    def _update_buffer(self):
        if self._model is not None:
            self._rtext.value = _convert_to_buf(self._model)
        else:
            self._rtext.value = []

    def _on_load_(self):
        pass

    def _back(self):
        Controller.board.show()

    def _write(self):
        Controller.resform.set_target(self._model)
        Controller.resform.show()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["thread"]["open_link"]:
                if not self._inputing_cmd:
                    self._cli = CommandLine(self._screen, "open:", self._open_link)
                    self._scene.add_effect(self._cli)
                return None

        return super().process_event(event)

    def _open_link(self, cmd: str):
        if str.isdecimal(cmd):
            idx = int(cmd)

            if len(self._model.links) > idx:
                link = self._model.links[idx]
                open_link(link)
        else:
            m = re.match(r'(\d+)-(\d+)', cmd)
            if m is not None:
                start_idx = int(m.group(1))
                end_idx = int(m.group(2))

                if start_idx < end_idx \
                        and start_idx >= 0 \
                        and end_idx < len(self._model.links):
                    open_links(self._model.links[start_idx:(end_idx + 1)])

        self._inputing_cmd = False


def _convert_to_buf(thread: Thread) -> Buffer:
    buf = []

    for i, r in enumerate(thread.responses):
        meta = []

        for c in str(r.number):
            meta.append((c, *THREAD_PALLET["normal"]))

        meta.append((" ", *THREAD_PALLET["normal"]))

        for c in r.name:
            meta.append((c, *THREAD_PALLET["name"]))

        meta.append((" ", *THREAD_PALLET["normal"]))

        for c in r.date:
            meta.append((c, *THREAD_PALLET["normal"]))

        meta.append((" ", *THREAD_PALLET["normal"]))

        for c in r.id:
            meta.append((c, *THREAD_PALLET["normal"]))

        buf.append(meta)
        buf.append([])

        for l in r.message.split("\n"):
            line = []

            for c in l:
                line.append((c, *THREAD_PALLET["normal"]))

            buf.append(line)

        buf.append([])

    return buf
