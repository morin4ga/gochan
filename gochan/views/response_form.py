from asciimatics.exceptions import NextScene
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, PopUpDialog, Text, TextBox, Widget

from gochan.client import post_response
from gochan.data import Thread
from gochan.state import app_state


class ResponseForm(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         on_load=self._load,
                         )

        self._target: Thread = None

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

    def _load(self):
        if self._target == app_state.res_form:
            return

        self._target = app_state.res_form
        self._clear_all_inputs()

    def _back(self):
        raise NextScene("Board")

    def _submit(self):
        if self._target is not None:
            self.save()
            name = self._name_box.value
            mail = self._mail_box.value
            msg = self._msg_box.value

            if len(msg) > 0:
                result = post_response(self._target.server, self._target.board, self._target.key, name, mail, msg)
                self._scene.add_effect(PopUpDialog(self._screen, result, ["Close"], theme="user_theme",
                                                   on_close=self._on_posted))
            else:
                self._scene.add_effect(PopUpDialog(self._screen, "メッセージが空です", ["Close"], theme="user_theme"))

    def _on_posted(self, _):
        self._clear_all_inputs()
        app_state.to_thread()

    def _clear_all_inputs(self):
        self._name_box.value = ""
        self._mail_box.value = ""
        self._msg_box.value = ""
