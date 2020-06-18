from typing import List

from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, TextBox, CheckBox, Layout, Widget, Divider, Button, DropdownList, Label,\
    VerticalDivider
from asciimatics.event import KeyboardEvent


class NGForm(Frame):
    def __init__(self, screen: Screen, on_close, board: str = None, key: str = None):
        """
        Parameters
        ----------
        on_close : (kind, use_reg, hide, value, board, key) -> None
        """
        super().__init__(screen,
                         int(screen.height * 0.8),
                         int(screen.width * 0.8),
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         )

        self.set_theme("user_theme")

        self._board = board
        self._key = key

        self._on_close = on_close

        scopes = [("全ての板", 0)]

        if board is not None:
            scopes.append((board, 1))

            if key is not None:
                scopes.append((board + "-" + key, 2))

        self._scope_drop = DropdownList(scopes, name="scope_drop")
        self._kind_drop = DropdownList([("title", 0), ("name", 1), ("id", 2),
                                        ("word", 3)], name="kind_drop")
        self._use_reg_chk = CheckBox("", name="use_reg_chk")
        self._hide_chk = CheckBox("", name="hide_chk")
        self._value_box = TextBox(Widget.FILL_COLUMN, name="value_box", as_string=True)

        self._save_btn = Button("Save", self._save_clicked)

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("scope"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._scope_drop, 2)

        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Divider())

        layout3 = Layout([10, 3, 87])
        self.add_layout(layout3)
        layout3.add_widget(Label("kind"), 0)
        layout3.add_widget(VerticalDivider(), 1)
        layout3.add_widget(self._kind_drop, 2)

        layout4 = Layout([100])
        self.add_layout(layout4)
        layout4.add_widget(Divider())

        layout5 = Layout([10, 3, 87])
        self.add_layout(layout5)
        layout5.add_widget(Label("use_reg"), 0)
        layout5.add_widget(VerticalDivider(), 1)
        layout5.add_widget(self._use_reg_chk, 2)

        layout6 = Layout([100])
        self.add_layout(layout6)
        layout6.add_widget(Divider())

        layout7 = Layout([10, 3, 87])
        self.add_layout(layout7)
        layout7.add_widget(Label("hide"), 0)
        layout7.add_widget(VerticalDivider(), 1)
        layout7.add_widget(self._hide_chk, 2)

        layout8 = Layout([100])
        self.add_layout(layout8)
        layout8.add_widget(Divider())

        layout9 = Layout([10, 3, 87], fill_frame=True)
        self.add_layout(layout9)
        layout9.add_widget(Label("value"), 0)
        layout9.add_widget(VerticalDivider(), 1)
        layout9.add_widget(self._value_box, 2)

        layout10 = Layout([100])
        self.add_layout(layout10)
        layout10.add_widget(Divider())

        layout11 = Layout([25, 25, 25, 25])
        self.add_layout(layout11)
        layout11.add_widget(self._save_btn)

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

        scope_idx = self.data.get("scope_drop")
        kind_idx = self.data.get("kind_drop")
        use_reg = self.data.get("use_reg_chk")
        hide = self.data.get("hide_chk")
        value = self.data.get("value_box")

        if scope_idx is not None and kind_idx is not None and use_reg is not None and hide is not None\
                and value is not None:

            board = None
            key = None

            if scope_idx == 1:
                board = self._board
            elif scope_idx == 2:
                board = self._board
                key = self._key

            if kind_idx == 0:
                kind = "title"
            elif kind_idx == 1:
                kind = "name"
            elif kind_idx == 2:
                kind = "id"
            elif kind_idx == 3:
                kind = "word"

            self.disappaer()
            self._on_close(kind, use_reg, hide, value, board, key)
