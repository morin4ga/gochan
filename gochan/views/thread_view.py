import re
from typing import Callable, List, Dict, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget

from gochan.browser import open_link, open_links
from gochan.config import BROWSER_PATH, KEY_BINDINGS, THREAD_BRUSHES
from gochan.models import Response
from gochan.view_models import ThreadVM
from gochan.effects import CommandLine
from gochan.widgets import Brush, Buffer, Cell, RichText
from wcwidth import wcwidth


def _gen_buffer(responses: List[Response], width: int, brushes: Dict[str, int]) -> Tuple[Buffer, List[Tuple[int, int]]]:
    """
    Parameters
    ----------
    width : int
    brush : {'normal', 'name'}

    Returns
    -------
    Buffer
    anchors : [(int, int)]
    List of tuple that represents the location of response by start/end line number
    """
    buf = Buffer(width)
    anchors = []
    link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')
    link_idx = 0

    for r in responses:
        anchors.append(len(buf))

        buf.push(str(r.number) + " ", brushes["normal"])

        buf.push(r.name, brushes["name"])

        buf.push(" " + r.date + " " + r.id, brushes["normal"])

        buf.break_line(2)

        # Add index suffix so that user can select url easily
        def _mark_link(match):
            nonlocal link_idx
            url = match.group(1)
            repl = url + "(" + str(link_idx) + ")"
            link_idx += 1
            return repl

        marked_msg = link_reg.sub(_mark_link, r.message)

        for l in marked_msg.split("\n"):
            buf.push(l, brushes["normal"])
            buf.break_line(1)

        buf.break_line(1)

    return (buf, anchors)


class ThreadView(Frame):
    def __init__(self, screen: Screen, data_context: ThreadVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self._data_context: ThreadVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)

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

    def update_buffer(self):
        if self._data_context.responses is None:
            return

        (self._rtext.value, self._anchors) = _gen_buffer(self._data_context.responses, self._rtext.width,
                                                         THREAD_BRUSHES)
        self._rtext.reset_offset()

    def _data_context_changed(self, property_name: str):
        if property_name == "responses":
            self.update_buffer()

    def _on_load_(self):
        pass

    def _on_back_btn_pushed(self):
        raise NextScene("Board")

    def _on_update_btn_pushed(self):
        self._data_context.update()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_write_btn_pushed(self):
        raise NextScene("ResponseForm")

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

            if self._data_context.links is not None and len(self._data_context.links) > idx:
                link = self._data_context.links[idx]
                open_link(link)
        else:
            m = re.match(r'(\d+)-(\d+)', cmd)
            if m is not None:
                start_idx = int(m.group(1))
                end_idx = int(m.group(2))

                if self._data_context.links is not None \
                        and start_idx < end_idx \
                        and start_idx >= 0 \
                        and end_idx < len(self._data_context.links):
                    open_links(self._data_context.links[start_idx:(end_idx + 1)])

        self._open_link_cli = None

    def _show_image(self, cmd: str):
        self._show_image_cli = None

        if cmd.isdecimal():
            idx = int(cmd)

            if self._data_context.links is not None and len(self._data_context.links) > idx:
                link = self._data_context.links[idx]

                if re.match(r'.*\.(jpg|png|jpeg|gif)', link) is not None:
                    self._data_context.set_image(link)
                    raise NextScene("Image")

    def _go_to(self, cmd: str):
        self._goto_cli = None

        if cmd.isdecimal():
            idx = int(cmd) - 1

            if idx >= 0 and idx < len(self._anchors):
                self._rtext.go_to(self._anchors[idx])
