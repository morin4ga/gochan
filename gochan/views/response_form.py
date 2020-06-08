from typing import Optional

from asciimatics.exceptions import NextScene
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, PopUpDialog, Text, TextBox, Widget

from gochan.models import Thread
from gochan.view_models import ResponseFormVM


class ResponseForm(Frame):
    def __init__(self, screen: Screen, data_context: ResponseFormVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         on_load=self._load,
                         )

        self._data_context: ResponseFormVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)

        self.set_theme("user_theme")

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

        self._back_button = Button("Back", on_click=self._back)
        self._submit_button = Button("Submit", on_click=self._submit)

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
        layout2.add_widget(self._back_button)
        layout2.add_widget(self._submit_button, 1)

        self.fix()

    def _data_context_changed(self, property_name: str):
        pass

    def _load(self):
        self._clear_all_inputs()

    def _back(self):
        raise NextScene("Thread")

    def _submit(self):
        self.save()
        name = self._name_box.value
        mail = self._mail_box.value
        msg = self._msg_box.value

        if len(msg) > 0:
            result = self._data_context.post(name, mail, msg)
            self._scene.add_effect(PopUpDialog(self._screen, result, ["Close"], theme="user_theme",
                                               on_close=self._on_posted))
        else:
            self._scene.add_effect(PopUpDialog(self._screen, "メッセージが空です", ["Close"], theme="user_theme"))

    def _on_posted(self, _):
        self._clear_all_inputs()
        self._data_context.update_thread()
        raise NextScene("Thread")

    def _clear_all_inputs(self):
        self._name_box.value = ""
        self._mail_box.value = ""
        self._msg_box.value = ""
