import re
from typing import List, Any

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, Widget, Label, PopUpDialog

from gochan.browser import open_link, open_links
from gochan.theme import THREAD_BRUSHES
from gochan.keybinding import KEY_BINDINGS
from gochan.view_models import ThreadVM
from gochan.effects import CommandLine, NGCreator, PostForm
from gochan.widgets import Buffer, Cell, RichText
from gochan.models.ng import NGResponse

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

        self._keybindings = KEY_BINDINGS["thread"]

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

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(self._title_label)
        layout.add_widget(Divider())

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
        if property_name == "responses" or property_name == "bookmark" or property_name == "ng":
            if self._data_context.responses is not None:
                self._update_buffer()

        # If responses is changed, update title and scroll to top of unread responses
        if property_name == "responses":
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

    def _collection_changed(self, property_name: str, kind: str, item: Any):
        if property_name == "responses":
            self._update_buffer()
            self._title_label.text = self._data_context.title + " (" + str(len(self._data_context.responses)) + ")"

    def _update_buffer(self):
        buf = Buffer(self._rtext.width)
        self._anchors = []
        link_idx = 0

        for r in self._data_context.filtered_responses:
            if isinstance(r, NGResponse):
                if r.hide:
                    self._anchors.append((len(buf), len(buf)))
                    continue
                else:
                    start = len(buf)
                    buf.push(str(r.origin.number) + " " + "あぼーん", THREAD_BRUSHES["normal"])
                    buf.break_line(1)
                    end = len(buf)
                    self._anchors.append((start, end))
                    buf.break_line(1)
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
        self._update_bookmark()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_write_btn_pushed(self):
        self._scene.add_effect(PostForm(self._screen, self._form_closed, "response"))

    def _form_closed(self, name: str, mail: str, msg: str):
        result = self._data_context.post(name, mail, msg)
        self._scene.add_effect(PopUpDialog(self._screen, result, ["Close"], theme="user_theme"))
        self._data_context.update()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == self._keybindings["open_link"]:
                self._scene.add_effect(CommandLine(self._screen, "open:", self._open_link))
                return None
            elif event.key_code == self._keybindings["show_image"]:
                self._scene.add_effect(CommandLine(self._screen, "show:", self._show_image))
                return None
            elif event.key_code == self._keybindings["go_to"]:
                self._scene.add_effect(CommandLine(self._screen, "go to:", self._go_to))
                return None
            elif event.key_code == self._keybindings["ng_name"]:
                self._scene.add_effect(CommandLine(self._screen, "ng name:", self._open_ngeditor_name))
                return None
            elif event.key_code == self._keybindings["ng_id"]:
                self._scene.add_effect(CommandLine(self._screen, "ng id:", self._open_ngeditor_id))
                return None
            elif event.key_code == self._keybindings["ng_word"]:
                self._scene.add_effect(CommandLine(self._screen, "ng word:", self._open_ngeditor_word))
                return None
            elif event.key_code == self._keybindings["update"]:
                self._data_context.update()
                self._update_bookmark()
                return None
            elif event.key_code == self._keybindings["back"]:
                self._update_bookmark()
                raise NextScene("Board")

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

    def _open_ngeditor_name(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_name,
                                                 self._data_context.responses[idx].name))

    def _add_ng_name(self, value, use_reg, hide, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_name(value, use_reg, hide, None, None)
        elif scope_idx == 1:
            self._data_context.add_ng_name(value, use_reg, hide, self._data_context.board, None)
        elif scope_idx == 2:
            self._data_context.add_ng_name(value, use_reg, hide, self._data_context.board, self._data_context.key)

    def _open_ngeditor_id(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_id, self._data_context.responses[idx].id))

    def _add_ng_id(self, value, use_reg, hide, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_id(value, use_reg, hide, None, None)
        elif scope_idx == 1:
            self._data_context.add_ng_id(value, use_reg, hide, self._data_context.board, None)
        elif scope_idx == 2:
            self._data_context.add_ng_id(value, use_reg, hide, self._data_context.board, self._data_context.key)

    def _open_ngeditor_word(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_word,
                                                 self._data_context.responses[idx].message))

    def _add_ng_word(self, value, use_reg, hide, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_word(value, use_reg, hide, None, None)
        elif scope_idx == 1:
            self._data_context.add_ng_word(value, use_reg, hide, self._data_context.board, None)
        elif scope_idx == 2:
            self._data_context.add_ng_word(value, use_reg, hide, self._data_context.board, self._data_context.key)

    def _update_bookmark(self):
        if self._data_context.bookmark is None:
            return

        displayed_end_line = self._rtext.scroll_offset + self._rtext._h

        new_bookmark = self._data_context.bookmark

        for number, (_, end) in enumerate(self._anchors, 1):
            if displayed_end_line >= end and self._data_context.bookmark < number:
                new_bookmark = number

        self._data_context.bookmark = new_bookmark
