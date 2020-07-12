from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, TextBox, CheckBox, Layout, Widget, Divider, Button, Label,\
    VerticalDivider


class NGEditor(Frame):
    def __init__(self, screen: Screen, default_values, on_close):
        super().__init__(screen,
                         int(screen.height * 0.8),
                         int(screen.width * 0.8),
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self.set_theme("user_theme")

        self._on_close = on_close

        self._board_text = Text()
        self._board_text.value = default_values.get("board") if default_values.get("board") is not None else ""

        self._key_text = Text()
        self._key_text.value = default_values.get("key") if default_values.get("key") is not None else ""

        self._use_reg_chk = CheckBox("")
        self._use_reg_chk.value = default_values.get("use_reg") if default_values.get("use_reg") is not None else False

        self._hide_chk = CheckBox("")
        self._hide_chk.value = default_values.get("hide") if default_values.get("hide") is not None else False

        self._auto_ng_id_chk = CheckBox("")
        self._auto_ng_id_chk.value = default_values.get(
            "auto_ng_id") if default_values.get("auto_ng_id") is not None else False

        self._value_text = TextBox(Widget.FILL_COLUMN, as_string=True)
        self._value_text.value = default_values.get("value") if default_values.get("value") is not None else ""

        self._save_btn = Button("Save", self._save_clicked)
        self._cancel_btn = Button("Cancel", self._cancel_clicked)

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("board"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._board_text, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("key"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._key_text, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("use_reg"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._use_reg_chk, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("hide"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._hide_chk, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("auto_ng_id"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._auto_ng_id_chk, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("value"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._value_text, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([5, 5])
        self.add_layout(layout)
        layout.add_widget(self._save_btn)
        layout.add_widget(self._cancel_btn, 1)

        self.fix()

    def disappaer(self):
        self._scene.remove_effect(self)

    def _cancel_clicked(self):
        self.disappaer()

    def _save_clicked(self):
        self.save()

        board = self._board_text.value
        key = self._key_text.value
        use_reg = self._use_reg_chk.value
        hide = self._hide_chk.value
        auto_ng_id = self._auto_ng_id_chk.value
        value = self._value_text.value

        board = None if board == "" else board
        key = None if key == "" else key

        d = {
            "board": board,
            "key": key,
            "use_reg": use_reg,
            "hide": hide,
            "auto_ng_id": auto_ng_id,
            "value": value
        }

        self.disappaer()
        self._on_close(d)


class NGTitleEditor(Frame):
    def __init__(self, screen: Screen, default_values, on_close):
        super().__init__(screen,
                         int(screen.height * 0.8),
                         int(screen.width * 0.8),
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True,
                         is_modal=True
                         )

        self.set_theme("user_theme")

        self._on_close = on_close

        self._board_text = Text()
        self._board_text.value = default_values.get("board") if default_values.get("board") is not None else ""

        self._use_reg_chk = CheckBox("")
        self._use_reg_chk.value = default_values.get("use_reg") if default_values.get("use_reg") is not None else False

        self._value_text = TextBox(Widget.FILL_COLUMN, as_string=True)
        self._value_text.value = default_values.get("value") if default_values.get("value") is not None else ""

        self._save_btn = Button("Save", self._save_clicked)
        self._cancel_btn = Button("Cancel", self._cancel_clicked)

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("board"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._board_text, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("use_reg"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._use_reg_chk, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([10, 3, 87], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("value"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._value_text, 2)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([5, 5])
        self.add_layout(layout)
        layout.add_widget(self._save_btn)
        layout.add_widget(self._cancel_btn, 1)

        self.fix()

    def disappaer(self):
        self._scene.remove_effect(self)

    def _cancel_clicked(self):
        self.disappaer()

    def _save_clicked(self):
        self.save()

        board = self._board_text.value
        use_reg = self._use_reg_chk.value
        hide = self._hide_chk.value
        value = self._value_text.value

        board = None if board == "" else board

        d = {
            "board": board,
            "use_reg": use_reg,
            "hide": hide,
            "value": value
        }

        self.disappaer()
        self._on_close(d)
