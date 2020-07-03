from typing import List, Tuple, Optional, Callable

from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, TextBox, CheckBox, Layout, Widget, Divider, Button, DropdownList, Label,\
    VerticalDivider, RadioButtons
from asciimatics.event import KeyboardEvent

from gochan.models.ng import NGItem


class NGCreator(Frame):
    def __init__(self, screen: Screen, on_close, kind: str, value: str, board: Optional[str] = None,
                 key: Optional[str] = None):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self.set_theme("user_theme")

        self._on_close = on_close
        self._board = board
        self._key = key
        self._kind = kind

        options = []

        if kind != "id":
            options.append(("全ての板", 0))
        if board is not None:
            options.append(("この板のみ", 1))
        if key is not None:
            options.append(("このスレのみ", 2))

        self._scope_radio = RadioButtons(options)

        self._use_reg_chk = CheckBox("")

        self._hide_chk = CheckBox("")

        self._value_box = TextBox(Widget.FILL_COLUMN, as_string=True)
        self._value_box.value = value

        self._save_btn = Button("Save", self._save_clicked)
        self._cancel_btn = Button("Cancel", lambda: self.disappaer())

        l = Layout([10, 3, 87])
        self.add_layout(l)
        l.add_widget(Label("scope"), 0)
        l.add_widget(VerticalDivider(), 1)
        l.add_widget(self._scope_radio, 2)

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
        l.add_widget(self._cancel_btn, 1)

        self.fix()

    def disappaer(self):
        self._scene.remove_effect(self)

    def _save_clicked(self):
        self.save()

        scope_idx = self._scope_radio.value
        use_reg = self._use_reg_chk.value
        hide = self._hide_chk.value
        value = self._value_box.value

        if value != "":
            board = None
            key = None
            if scope_idx == 1:
                board = self._board
            if scope_idx == 2:
                board = self._board
                key = self._key

            self.disappaer()
            self._on_close(self._kind, value, use_reg, hide, board, key)
