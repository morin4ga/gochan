from typing import Dict, List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Widget
from wcwidth import wcswidth, wcwidth

# [(ch, fg, att, bg)]
Cell = Tuple[str, int, int, int]
Buffer = List[List[Cell]]


class RichText(Widget):
    def __init__(self, height, flush_cell: Cell, keybindings: Dict[str, int], **kwargs):
        super().__init__(**kwargs)
        self._required_height = height
        self._scrl_offset = 0
        self._value = []
        self._fc = flush_cell
        self._keybindings = keybindings

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
        pass

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == self._keybindings["scroll_down"]:
                self.scroll_down()
                return None
            elif event.key_code == self._keybindings["scroll_up"]:
                self.scroll_up()
                return None
            elif event.key_code == self._keybindings["page_up"]:
                self.page_up()
                return None
            elif event.key_code == self._keybindings["page_down"]:
                self.page_down()
                return None
            elif event.key_code == self._keybindings["go_to_top"]:
                self.go_to_top()
                return None
            elif event.key_code == self._keybindings["go_to_bottom"]:
                self.go_to_bottom()
                return None

        return event

    def scroll_down(self):
        max_offset = len(self._value) - self._h

        if self._scrl_offset < max_offset:
            self._scrl_offset += 1

    def scroll_up(self):
        if self._scrl_offset > 0:
            self._scrl_offset -= 1

    def page_up(self):
        if self._scrl_offset - self._h < 0:
            self._scrl_offset = 0
        else:
            self._scrl_offset -= self._h

    def page_down(self):
        max_offset = len(self._value) - self._h

        if self._scrl_offset + self._h < max_offset:
            self._scrl_offset += self._h
        else:
            self._scrl_offset = max_offset

    def go_to_top(self):
        self._scrl_offset = 0

    def go_to_bottom(self):
        self._scrl_offset = len(self._value) - self._h

    def go_to(self, line):
        max_offset = len(self._value) - self._h

        if line == 0:
            self._scrl_offset = 0
        elif line - 1 > max_offset:
            self._scrl_offset = max_offset
        else:
            self._scrl_offset = line - 1

    def required_height(self, offset, width):
        return self._required_height

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: Buffer):
        self._value = new_value
