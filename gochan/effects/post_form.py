from asciimatics.exceptions import NextScene
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, PopUpDialog, Text, TextBox, Widget


class PostForm(Frame):
    def __init__(self, screen: Screen, on_close, mode: str):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         )

        self.set_theme("user_theme")

        self._on_close = on_close

        self._name_box = Text(
            label="name:",
            name="name_box",
        )

        self._mail_box = Text(
            label="mail:",
            name="mail_box"
        )

        self._msg_box = TextBox(
            Widget.FILL_COLUMN,
            as_string=True,
            label="msg :",
            name="msg_box"
        )

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._name_box)
        layout1.add_widget(Divider())
        layout1.add_widget(self._mail_box)
        layout1.add_widget(Divider())
        layout1.add_widget(self._msg_box)
        layout1.add_widget(Divider())

        layout2 = Layout([5, 5])
        self.add_layout(layout2)
        layout2.add_widget(Button("Submit", self._submit_clicked))
        layout2.add_widget(Button("Cancel", self._cancel_clicked), 1)

        self.fix()

    def disappear(self):
        self._scene.remove_effect(self)

    def _cancel_clicked(self):
        self.disappear()

    def _submit_clicked(self):
        self.save()
        name = self._name_box.value
        mail = self._mail_box.value
        msg = self._msg_box.value

        if len(msg) > 0:
            self.disappear()
            self._on_close(name, mail, msg)
        else:
            self._scene.add_effect(PopUpDialog(self._screen, "メッセージが空です", ["Close"], theme="user_theme"))
