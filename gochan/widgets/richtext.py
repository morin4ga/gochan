from typing import List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Widget
from wcwidth import wcswidth, wcwidth

# [(ch, fg, att, bg)]
Cell = Tuple[str, int, int, int]
Buffer = List[List[Cell]]


class RichText(Widget):
    def __init__(self, height, flush_cell: Cell, **kwargs):
        super().__init__(**kwargs)
        self._required_height = height
        self._scrl_offset = 0
        self._value = []
        self._fc = flush_cell

    def update(self, frame_no):
        for i in range(self._h):
            self._frame.canvas.print_at(
                self._fc[0] * self.width,
                self._x,
                self._y + i,
                self._fc[1], self._fc[2], self._fc[3])

        max_x = self._w + self._x - 1
        max_y = self._h + self._y - 1
        x = self._x
        y = self._y

        for l in self._value[self._scrl_offset:]:
            if y > max_y:
                break

            for c in l:
                w = wcwidth(c[0])

                if x + w > max_x:
                    break

                self._frame.canvas.print_at(c[0], x, y, c[1], c[2], c[3])
                x += w

            x = self._x
            y += 1

    def reset(self):
        self._scrl_offset = 0

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_DOWN:
                max_offset = len(self._value) - self._h

                if self._scrl_offset < max_offset:
                    self._scrl_offset += 1

                return None

            elif event.key_code == Screen.KEY_UP:
                if self._scrl_offset > 0:
                    self._scrl_offset -= 1

                return None

        return event

    def required_height(self, offset, width):
        return self._required_height

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: Buffer):
        self._value = new_value
