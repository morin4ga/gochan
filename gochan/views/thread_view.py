import re
from typing import Callable, List, Dict, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, TextBox, Widget, Label, PopUpDialog

from gochan.browser import open_link, open_links
from gochan.config import BROWSER_PATH, THREAD_BRUSHES
from gochan.keybinding import KEY_BINDINGS
from gochan.models import Response
from gochan.view_models import ThreadVM
from gochan.effects import CommandLine, NGCreator, PostForm
from gochan.widgets import Brush, Buffer, Cell, RichText
from wcwidth import wcwidth

link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')


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
        self._data_context.on_collection_changed.add(self._collection_changed)

        self._anchors: List[int] = None

        self.set_theme("user_theme")

        self._title_label = Label("")

        self._rtext = RichText(
            Widget.FILL_FRAME,
            Cell(" ", THREAD_BRUSHES["normal"]),
            KEY_BINDINGS["thread"],
            name="text_box",
        )

        self._back_button = Button("Back", on_click=self._on_back_btn_pushed)
        self._update_button = Button("Update", on_click=self._on_update_btn_pushed)
        self._write_button = Button("Write", on_click=self._on_write_btn_pushed)

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(self._title_label)
        l.add_widget(Divider())

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

    def _data_context_changed(self, property_name: str):
        if property_name == "responses" or property_name == "ng":
            if self._data_context.responses is None:
                return

            self._update_buffer()

            self._title_label.text = self._data_context.title + " (" + str(len(self._data_context.responses)) + ")"

            bookmark = self._data_context.bookmark

            if bookmark != 0:
                # if there are unread responses, then scroll to them
                if len(self._anchors) > bookmark:
                    line = self._anchors[bookmark][0]
                    self._rtext.go_to(line)
                else:
                    self._rtext.go_to(self._anchors[bookmark - 1][0])
            else:
                self._rtext.reset_offset()

    def _collection_changed(self, args):
        property_name, kind, arg = args

        if property_name == "responses":
            self._update_buffer()

    def _update_buffer(self):
        buf = Buffer(self._rtext.width)
        self._anchors = []
        link_idx = 0

        for r in self._data_context.responses:
            mode = self._data_context.ng.is_ng(r, self._data_context.board, self._data_context.key)

            if mode == 1:
                start = len(buf)
                buf.push(str(r.number) + " " + "あぼーん", THREAD_BRUSHES["normal"])
                buf.break_line(1)
                end = len(buf)
                self._anchors.append((start, end))
                buf.break_line(1)
                continue
            elif mode == 2:
                self._anchors.append((len(buf), len(buf)))
                continue

            start = len(buf)

            buf.push(str(r.number) + " ", THREAD_BRUSHES["normal"])

            buf.push(r.name, THREAD_BRUSHES["name"])

            buf.push(" " + r.date + " " + r.id, THREAD_BRUSHES["normal"])

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
                buf.push(l, THREAD_BRUSHES["normal"])
                buf.break_line(1)

            end = len(buf)

            self._anchors.append((start, end))

            buf.break_line(1)

            # don't render bookmark if bookmark points last response
            if r.number == self._data_context.bookmark and \
                    len(self._data_context.responses) != self._data_context.bookmark:
                buf.push("─" * self._rtext.width, THREAD_BRUSHES["bookmark"])
                buf.break_line(2)

        self._rtext.value = buf

    def _on_load_(self):
        pass

    def _on_back_btn_pushed(self):
        self._update_bookmark()
        raise NextScene("Board")

    def _on_update_btn_pushed(self):
        self._data_context.update()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_write_btn_pushed(self):
        self._scene.add_effect(PostForm(self._screen, self._form_closed, "response"))

    def _form_closed(self, name: str, mail: str, msg: str):
        result = self._data_context.post(name, mail, msg)
        self._scene.add_effect(PopUpDialog(self._screen, result, ["Close"], theme="user_theme"))
        self._data_context.update()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["thread"]["open_link"]:
                if len(self._scene.effects) == 1:
                    # If any effects except this frame are not opened
                    self._scene.add_effect(CommandLine(self._screen, "open:", self._open_link))
                return None
            elif event.key_code == ord("a"):
                if len(self._scene.effects) == 1:
                    self._scene.add_effect(CommandLine(self._screen, "show:", self._show_image))
                return None
            elif event.key_code == ord("g"):
                if len(self._scene.effects) == 1:
                    self._scene.add_effect(CommandLine(self._screen, "go to:", self._go_to))
                return None
            elif event.key_code == ord("n"):
                if len(self._scene.effects) == 1:
                    self._scene.add_effect(CommandLine(self._screen, "ng name:", self._add_ng_name))
                return None
            elif event.key_code == ord("i"):
                if len(self._scene.effects) == 1:
                    self._scene.add_effect(CommandLine(self._screen, "ng id:", self._add_ng_id))
                return None
            elif event.key_code == ord("w"):
                if len(self._scene.effects) == 1:
                    self._scene.add_effect(CommandLine(self._screen, "ng word:", self._add_ng_word))
                return None

        return super().process_event(event)

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

    def _show_image(self, cmd: str):
        if cmd.isdecimal():
            idx = int(cmd)

            if self._data_context.links is not None and len(self._data_context.links) > idx:
                link = self._data_context.links[idx]

                if re.match(r'.*\.(jpg|png|jpeg|gif)', link) is not None:
                    self._data_context.set_image(link)
                    self._update_bookmark()
                    raise NextScene("Image")

    def _go_to(self, cmd: str):
        if cmd.isdecimal():
            idx = int(cmd) - 1

            if idx >= 0 and idx < len(self._anchors):
                self._rtext.go_to(self._anchors[idx][0])

    def _add_ng_name(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._data_context.ng.insert, "name",
                                                 self._data_context.responses[idx].name, self._data_context.board,
                                                 self._data_context.key))

    def _add_ng_id(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._data_context.ng.insert, "id",
                                                 self._data_context.responses[idx].id, self._data_context.board,
                                                 self._data_context.key))

    def _add_ng_word(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._data_context.ng.insert, "word",
                                                 self._data_context.responses[idx].message, self._data_context.board,
                                                 self._data_context.key))

    def _update_bookmark(self):
        if self._data_context.bookmark is None:
            return

        displayed_end_line = self._rtext.scroll_offset + self._rtext._h

        for number, (_, end) in enumerate(self._anchors, 1):
            if displayed_end_line >= end and self._data_context.bookmark < number:
                self._data_context.bookmark = number
