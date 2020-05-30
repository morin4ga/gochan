import re
from typing import Callable, List

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget

from gochan.browser import open_link, open_links
from gochan.config import BROWSER_PATH, KEY_BINDINGS, THREAD_BRUSHES
from gochan.controller import controller
from gochan.view_models import ThreadVM
from gochan.effects import CommandLine
from gochan.widgets import Brush, Buffer, Cell, RichText
from wcwidth import wcwidth


class ThreadView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self._model: ThreadVM = None

        self._anchors: List[int] = None

        self._open_link_cli = None
        self._show_image_cli = None
        self._goto_cli = None

        self.set_theme("user_theme")

        self._rtext = RichText(
            Widget.FILL_FRAME,
            Cell(" ", THREAD_BRUSHES["normal"]),
            KEY_BINDINGS["thread"],
            name="text_box",
        )

        self._back_button = Button("Back", on_click=self._on_back_btn_pushed)
        self._update_button = Button("Update", on_click=self._on_update_btn_pushed)
        self._write_button = Button("Write", on_click=self._on_write_btn_pushed)

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._rtext)
        layout1.add_widget(Divider())

        layout2 = Layout([33, 33, 34])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)
        layout2.add_widget(self._update_button, 1)
        layout2.add_widget(self._write_button, 2)

        self.fix()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: ThreadVM):
        self._model = model
        (buf, anchors) = model.to_buffer(self._rtext.width, THREAD_BRUSHES)
        self._anchors = anchors
        self._rtext.value = buf
        self._rtext.reset_offset()

    def _on_load_(self):
        pass

    def _on_back_btn_pushed(self):
        raise NextScene(controller.board.scene_name)

    def _on_update_btn_pushed(self):
        controller.thread.update_data()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_write_btn_pushed(self):
        controller.resform.set_target(self._model)
        raise NextScene(controller.resform.scene_name)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["thread"]["open_link"]:
                if not self._is_cli_opened():
                    self._open_link_cli = CommandLine(self._screen, "open:", self._open_link)
                    self._scene.add_effect(self._open_link_cli)
                return None
            elif event.key_code == ord("a"):
                if not self._is_cli_opened():
                    self._show_image_cli = CommandLine(self._screen, "show:", self._show_image)
                    self._scene.add_effect(self._show_image_cli)
                return None
            elif event.key_code == ord("g"):
                if not self._is_cli_opened():
                    self._goto_cli = CommandLine(self._screen, "go to:", self._go_to)
                    self._scene.add_effect(self._goto_cli)
                return None

        return super().process_event(event)

    def _is_cli_opened(self):
        return self._open_link_cli is not None\
            or self._show_image_cli is not None\
            or self._goto_cli is not None

    def _open_link(self, cmd: str):
        if cmd.isdecimal():
            idx = int(cmd)

            if len(self._model.links) > idx:
                link = self._model.links[idx]
                open_link(link)
        else:
            m = re.match(r'(\d+)-(\d+)', cmd)
            if m is not None:
                start_idx = int(m.group(1))
                end_idx = int(m.group(2))

                if start_idx < end_idx \
                        and start_idx >= 0 \
                        and end_idx < len(self._model.links):
                    open_links(self._model.links[start_idx:(end_idx + 1)])

        self._open_link_cli = None

    def _show_image(self, cmd: str):
        self._show_image_cli = None

        if cmd.isdecimal():
            idx = int(cmd)

            if len(self._model.links) > idx:
                link = self._model.links[idx]

                if re.match(r'.*\.(jpg|png|jpeg|gif)', link) is not None:
                    controller.image.set_image(link)
                    raise NextScene(controller.image.scene_name)

    def _go_to(self, cmd: str):
        self._goto_cli = None

        if cmd.isdecimal():
            idx = int(cmd) - 1

            if idx >= 0 and idx < len(self._anchors):
                self._rtext.go_to(self._anchors[idx])
