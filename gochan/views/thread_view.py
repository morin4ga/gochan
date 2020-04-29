from typing import Callable

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget

from gochan.data import Thread
from gochan.style import style
from gochan.widgets import Buffer, RichText


class ThreadView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
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

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._rtext)
        layout1.add_widget(Divider())

        layout2 = Layout([33, 33, 34])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)

        self.fix()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Thread):
        self._model = model
        self._rtext.reset()
        self._rtext.value = self._convert_to_buf(model)

    def _back(self):
        raise NextScene("Board")

    def _convert_to_buf(self, thread: Thread) -> Buffer:
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
