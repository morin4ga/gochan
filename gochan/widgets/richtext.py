from typing import Dict, List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Widget
from wcwidth import wcswidth, wcwidth


class Brush:
    def __init__(self, fg: int, bg: int, att: int):
        super().__init__()
        self.fg = fg
        self.bg = bg
        self.att = att


class Cell:
    def __init__(self, ch: str, brush: Brush):
        super().__init__()
        self.ch = ch
        self.brush = brush


class Buffer:
    def __init__(self, width: int):
        super().__init__()
        self.max_width = width
        self._list: List[List[Cell]] = []
        self._width = 0

    def push(self, s: str, brush: Brush):
        for c in s:
            self._push_cell(Cell(c, brush))

    def _push_cell(self, cell: Cell):
        if len(self._list) == 0:
            self._list.append([])

        w = wcwidth(cell.ch)

        if w > self.max_width:
            return

        if self._width + w > self.max_width:
            self._list.append([])
            self._width = 0

        self._list[len(self._list) - 1].append(cell)
        self._width += w

    def break_line(self, times: int):
        if len(self._list) == 0:
            self._list.append([])

        for _ in range(times):
            self._list.append([])
            self._width = 0

    def extend(self, buf: "Buffer"):
        self._list.extend(buf)

    def __delitem__(self, key):
        self._list.__delitem__(key)

    def __getitem__(self, key):
        return self._list.__getitem__(key)

    def __setitem__(self, key, value):
        self.__setitem__(key, value)

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()


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
                self._fc.ch * self.width,
                self._x,
                self._y + i,
                self._fc.brush.fg, self._fc.brush.att, self._fc.brush.bg)

        max_x = self._w + self._x - 1
        max_y = self._h + self._y - 1
        x = self._x
        y = self._y

        for l in self._value[self._scrl_offset:]:
            if y > max_y:
                break

            for c in l:
                w = wcwidth(c.ch)

                if x + w - 1 > max_x:
                    break

                self._frame.canvas.print_at(c.ch, x, y, c.brush.fg, c.brush.att, c.brush.bg)
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

    def reset_offset(self):
        self._scrl_offset = 0

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
        """
        Parameters
        ----------
        line : int
            Zero-based line number
        """

        max_offset = len(self._value) - self._h

        if line <= 0:
            self._scrl_offset = 0
        elif line > max_offset:
            self._scrl_offset = max_offset
        else:
            self._scrl_offset = line

    def required_height(self, offset, width):
        return self._required_height

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: Buffer):
        self._value = new_value
