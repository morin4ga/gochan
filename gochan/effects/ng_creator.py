from typing import Optional

from asciimatics.screen import Screen
from asciimatics.widgets import Frame, TextBox, CheckBox, Layout, Widget, Divider, Button, Label,\
    VerticalDivider, RadioButtons, PopUpDialog


class NGCreator(Frame):
    def __init__(self, screen: Screen, on_close, default_value: str,
                 key: Optional[str] = None):
        """
        Parameters
        ----------
        on_close : (value: str, use_reg: bool, hide: bool, scope_idx: int) -> None
                   scope_idx : 0 - 全ての板
                               1 - この板のみ
                               2 - このスレのみ
        """

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

        self._scope_radio = RadioButtons([("全ての板", 0), ("この板のみ", 1), ("このスレのみ", 2)])

        self._use_reg_chk = CheckBox("")

        self._hide_chk = CheckBox("")

        self._value_box = TextBox(Widget.FILL_COLUMN, as_string=True)
        self._value_box.value = default_value

        self._save_btn = Button("Save", self._save_clicked)
        self._cancel_btn = Button("Cancel", lambda: self.disappaer())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("scope"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._scope_radio, 2)

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

        layout = Layout([10, 3, 87], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("value"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._value_box, 2)

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

    def _save_clicked(self):
        self.save()

        scope_idx = self._scope_radio.value
        use_reg = self._use_reg_chk.value
        hide = self._hide_chk.value
        value = self._value_box.value

        if value != "":
            self.disappaer()
            self._on_close(value, use_reg, hide, scope_idx)
        else:
            self._scene.add_effect(PopUpDialog(self._screen, "valueが空です", ["Close"]))


class NGTitleCreator(Frame):
    def __init__(self, screen: Screen, on_close, default_value):
        """
        Parameters
        ----------
        on_close : (value: str, use_reg: bool, scope_idx: int) -> None
                   scope_idx : 0 - 全ての板
                               1 - この板のみ
        """

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

        self._scope_radio = RadioButtons([("全ての板", 0), ("この板のみ", 1)])

        self._use_reg_chk = CheckBox("")

        self._value_box = TextBox(Widget.FILL_COLUMN, as_string=True)
        self._value_box.value = default_value

        self._save_btn = Button("Save", self._save_clicked)
        self._cancel_btn = Button("Cancel", lambda: self.disappaer())

        layout = Layout([10, 3, 87])
        self.add_layout(layout)
        layout.add_widget(Label("scope"), 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._scope_radio, 2)

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
        layout.add_widget(self._value_box, 2)

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

    def _save_clicked(self):
        self.save()

        scope_idx = self._scope_radio.value
        use_reg = self._use_reg_chk.value
        value = self._value_box.value

        if value != "":
            self.disappaer()
            self._on_close(value, use_reg, scope_idx)
        else:
            self._scene.add_effect(PopUpDialog(self._screen, "valueが空です", ["Close"]))
