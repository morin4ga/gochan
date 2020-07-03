from typing import List, Tuple, Callable, Dict, Any

from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, TextBox, CheckBox, Layout, Widget, Divider, Button, DropdownList, Label,\
    VerticalDivider
from asciimatics.event import KeyboardEvent

from gochan.models.ng import NGItem


class NGEditor(Frame):
    def __init__(self, screen: Screen, item: NGItem, on_close: Callable[[Dict[str, Any]], None]):
        super().__init__(screen,
                         int(screen.height * 0.8),
                         int(screen.width * 0.8),
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self.set_theme("user_theme")

        self._item = item
        self._on_close = on_close

        self._board_text = Text(name="board_text")
        self._board_text.value = item.board
        self._key_text = Text(name="key_text")
        self._key_text.value = item.key

        self._kind_drop = DropdownList([("title", 0), ("name", 1), ("id", 2),
                                        ("word", 3)], name="kind_drop")

        if item.kind == "title":
            self._kind_drop.value = 0
        elif item.kind == "name":
            self._kind_drop.value = 1
        elif item.kind == "id":
            self._kind_drop.value = 2
        elif item.kind == "word":
            self._kind_drop.value = 3

        self._use_reg_chk = CheckBox("", name="use_reg_chk")
        self._use_reg_chk.value = item.use_reg

        self._hide_chk = CheckBox("", name="hide_chk")
        self._hide_chk.value = item.hide

        self._value_box = TextBox(Widget.FILL_COLUMN, name="value_box", as_string=True)
        self._value_box.value = item.value

        self._save_btn = Button("Save", self._save_clicked)

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("board"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._board_text, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("key"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._key_text, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("kind"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._kind_drop, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("use_reg"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._use_reg_chk, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("hide"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._hide_chk, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([10, 3, 87], fill_frame=True)
        self.add_layout(l)
        l.add_widget(Label("value"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._value_box, 2)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(Divider())

        l = Layout([25, 25, 25, 25])
        self.add_layout(l)
        l.add_widget(self._save_btn)

        self.fix()

    def disappaer(self):
        self._scene.remove_effect(self)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('q'):
                self.disappaer()
                return None

        super().process_event(event)

    def _save_clicked(self):
        self.save()

        board = self.data.get("board_text")
        key = self.data.get("key_text")
        kind_idx = self.data.get("kind_drop")
        use_reg = self.data.get("use_reg_chk")
        hide = self.data.get("hide_chk")
        value = self.data.get("value_box")

        if board is None:
            raise Exception("none")

        if board is not None and key is not None and kind_idx is not None and use_reg is not None \
                and hide is not None and value is not None:

            board = None if board == "" else board
            key = None if key == "" else key

            kind = None
            if kind_idx == 0:
                kind = "title"
            elif kind_idx == 1:
                kind = "name"
            elif kind_idx == 2:
                kind = "id"
            elif kind_idx == 3:
                kind = "word"

            d = {
                "board": board,
                "key": key,
                "kind": kind,
                "use_reg": use_reg,
                "hide": hide,
                "value": value
            }

            self.disappaer()
            self._on_close(d)
