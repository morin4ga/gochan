from asciimatics.widgets import Frame, Widget, Layout, TextBox, Button
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from data import Thread
from typing import Callable


class ThreadView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self._model: Thread = None

        self._text_box = TextBox(
            Widget.FILL_FRAME,
            name="text_box",
            line_wrap=False,
            as_string=True,
        )

        self._text_box.disabled = True

        self._back_button = Button("Back", on_click=self._back)
        self._up_button = Button("Scroll up", on_click=self._scroll_up)
        self._down_button = Button("Scroll down", on_click=self._scroll_down)

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._text_box)

        layout2 = Layout([33, 33, 34])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)
        layout2.add_widget(self._up_button, 1)
        layout2.add_widget(self._down_button, 2)

        self.fix()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Thread):
        self._model = model
        self._text_box.value = self._model.to_text()
        self._text_box._line = 0

    def _back(self):
        raise NextScene("Board")

    def _scroll_up(self):
        start_line = self._text_box._start_line
        cur_line = self._text_box._line

        self._text_box._change_line(-1 + -(cur_line - start_line))

    def _scroll_down(self):
        box_h = self._text_box._h
        cur_line = self._text_box._line
        start_line = self._text_box._start_line
        end_line = start_line + (box_h - 1)

        self._text_box._change_line(1 + end_line - cur_line)

    def _go_to_top(self):
        self._text_box._change_line(-self._text_box._line)

    def _go_to_bottom(self):
        self._text_box._change_line(len(self._text_box._value) - self._text_box._line)

    def handle_event(self, e: KeyboardEvent):
        c = e.key_code

        if c == Screen.ctrl("n"):
            self._scroll_down()
        elif c == Screen.ctrl("h"):
            self._scroll_up()
        elif c == Screen.ctrl("y"):
            self._go_to_top()
        elif c == Screen.ctrl("b"):
            self._go_to_bottom()
