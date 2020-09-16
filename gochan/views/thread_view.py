import re
from typing import List

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Label, Layout, PopUpDialog, Widget

from gochan.browser import open_link, open_links
from gochan.effects.command_line import CommandLine
from gochan.effects.ng_creator import NGCreator
from gochan.effects.post_form import PostForm
from gochan.effects.responses_popup import ResponsesPopup
from gochan.effects.help import Help
from gochan.event_handler import CollectionChangedEventArgs, PropertyChangedEventArgs
from gochan.keybinding import KEY_BINDINGS
from gochan.theme import THREAD_BRUSHES
from gochan.view_models.threadvm import ThreadVM
from gochan.widgets.responses_viewer import ResponsesViewer

link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')


class ThreadView(Frame):
    def __init__(self, screen: Screen, data_context: ThreadVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self._keybindings = KEY_BINDINGS["thread"]

        self._data_context: ThreadVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)

        self._anchors: List[int] = None

        self.set_theme("user_theme")

        self._title_label = Label("")

        self._responses_viewer = ResponsesViewer(
            Widget.FILL_FRAME,
            THREAD_BRUSHES,
            KEY_BINDINGS["thread"],
        )

        self._back_button = Button("Back", on_click=self._on_back_btn_pushed)
        self._update_button = Button("Update", on_click=self._on_update_btn_pushed)
        self._write_button = Button("Write", on_click=self._on_write_btn_pushed)

        layout = Layout([20, 20, 20, 20, 20])
        self.add_layout(layout)
        layout.add_widget(Button("Bbsmenu", self._to_bbsmenu), 0)
        layout.add_widget(Button("Board", self._to_board), 1)
        layout.add_widget(Button("Thread", None, disabled=True), 2)
        layout.add_widget(Button("Favorite", self._to_favorites), 3)
        layout.add_widget(Button("NG", self._to_ng), 4)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(self._title_label)
        layout.add_widget(Divider())

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._responses_viewer)
        layout1.add_widget(Divider())

        layout2 = Layout([33, 33, 34])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)
        layout2.add_widget(self._update_button, 1)
        layout2.add_widget(self._write_button, 2)

        self.fix()

    def _data_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "bookmark" or e.property_name == "ng":
            if self._data_context.responses is not None:
                self._responses_viewer.set_data(self._data_context.responses,
                                                self._data_context.replies, self._data_context.ids,
                                                self._data_context.bookmark)
        elif e.property_name == "responses":
            # If responses is changed, update title and scroll to top of unread responses

            if self._data_context.responses is not None:
                self._responses_viewer.set_data(self._data_context.responses,
                                                self._data_context.replies, self._data_context.ids,
                                                self._data_context.bookmark)
                self._update_title()
                self._responses_viewer.scroll_to_bookmark()
        elif e.property_name == "is_favorite":
            self._update_title()

    def _collection_changed(self, e: CollectionChangedEventArgs):
        if e.property_name == "responses":
            self._update_buffer()
            self._update_title()

    def _update_title(self):
        title = ""
        if self._data_context.title is not None and self._data_context.responses is not None:
            title = self._data_context.title + " (" + str(len(self._data_context.responses)) + ")"

        if self._data_context.is_favorite:
            title += " ★"

        self._title_label.text = title

    def _on_load(self):
        self.switch_focus(self._layouts[3], 0, 0)

    def _on_back_btn_pushed(self):
        self._save_history()
        raise NextScene("Board")

    def _on_update_btn_pushed(self):
        self._data_context.update()
        self._save_history()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_write_btn_pushed(self):
        self._scene.add_effect(PostForm(self._screen, self._form_closed, "response"))

    def _form_closed(self, name: str, mail: str, msg: str):
        result = self._data_context.post(name, mail, msg)
        self._scene.add_effect(PopUpDialog(self._screen, result, ["Close"], theme="user_theme"))
        self._data_context.update()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["global"]["help"].value:
                self._scene.add_effect(Help(self.screen))
                return None
            elif event.key_code == self._keybindings["open_link"].value:
                self._scene.add_effect(CommandLine(self._screen, "open:", self._open_link))
                return None
            elif event.key_code == self._keybindings["show_image"].value:
                self._scene.add_effect(CommandLine(self._screen, "show:", self._show_image))
                return None
            elif event.key_code == self._keybindings["go_to"].value:
                self._scene.add_effect(CommandLine(self._screen, "go to:", self._go_to))
                return None
            elif event.key_code == self._keybindings["ng_name"].value:
                self._scene.add_effect(CommandLine(self._screen, "ng name:", self._open_ngeditor_name))
                return None
            elif event.key_code == self._keybindings["ng_id"].value:
                self._scene.add_effect(CommandLine(self._screen, "ng id:", self._open_ngeditor_id))
                return None
            elif event.key_code == self._keybindings["ng_word"].value:
                self._scene.add_effect(CommandLine(self._screen, "ng word:", self._open_ngeditor_word))
                return None
            elif event.key_code == self._keybindings["update"].value:
                self._data_context.update()
                self._save_history()
                return None
            elif event.key_code == self._keybindings["back"].value:
                self._save_history()
                raise NextScene("Board")
            elif event.key_code == self._keybindings["favorite"].value:
                self._data_context.favorite()
            elif event.key_code == KEY_BINDINGS["thread"]["show_replies"].value:
                self._scene.add_effect(CommandLine(self._screen, "show_replies:", self._show_replies))
                return None
            elif event.key_code == KEY_BINDINGS["thread"]["show_response"].value:
                self._scene.add_effect(CommandLine(self._screen, "show_response:", self._show_respones))
                return None
            elif event.key_code == KEY_BINDINGS["thread"]["extract_id"].value:
                self._scene.add_effect(CommandLine(self._screen, "extract_id:", self._extract_id))
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
                    self._save_history()
                    raise NextScene("Image")

    def _go_to(self, cmd: str):
        if cmd.isdecimal():
            self._responses_viewer.jump_to(int(cmd))

    def _open_ngeditor_name(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_name,
                                                 self._data_context.responses[idx].name, "name"))

    def _show_replies(self, number: str):
        if self._data_context.replies is not None and number.isdecimal():
            number = int(number)
            if number in self._data_context.replies:
                replies = self._data_context.replies[number]
                self._scene.add_effect(ResponsesPopup(self._screen, THREAD_BRUSHES, KEY_BINDINGS["thread"],
                                                      replies, self._data_context.replies, self._data_context.ids,
                                                      self._show_replies, self._show_respones, self._extract_id))

    def _show_respones(self, number: str):
        if self._data_context.responses is not None and number.isdecimal():
            idx = int(number) - 1

            if len(self._data_context.responses) > idx and idx >= 0:
                respones = self._data_context.responses[idx]
                self._scene.add_effect(ResponsesPopup(self._screen, THREAD_BRUSHES,
                                                      KEY_BINDINGS["thread"], [
                                                          respones], self._data_context.replies, self._data_context.ids,
                                                      self._show_replies, self._show_respones, self._extract_id))

    def _extract_id(self, number: str):
        if self._data_context.responses is not None and number.isdecimal():
            idx = int(number) - 1

            if len(self._data_context.responses) > idx and idx >= 0:
                id = self._data_context.responses[idx].id
                if id in self._data_context.ids:
                    self._scene.add_effect(ResponsesPopup(self._screen, THREAD_BRUSHES,
                                                          KEY_BINDINGS["thread"], self._data_context.ids[id],
                                                          self._data_context.replies, self._data_context.ids,
                                                          self._show_replies, self._show_respones, self._extract_id))

    def _add_ng_name(self, value, use_reg, hide, auto_ng_id, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_name(value, use_reg, hide, auto_ng_id, None, None)
        elif scope_idx == 1:
            self._data_context.add_ng_name(value, use_reg, hide, auto_ng_id, self._data_context.board, None)
        elif scope_idx == 2:
            self._data_context.add_ng_name(value, use_reg, hide, auto_ng_id,
                                           self._data_context.board, self._data_context.key)

    def _open_ngeditor_id(self, number: str):
        if number.isdecimal():
            idx = int(number) - 1

            if self._data_context.responses is not None \
                    and len(self._data_context.responses) > idx \
                    and idx >= 0:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_id,
                                                 self._data_context.responses[idx].id, "id"))

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
                                                 self._data_context.responses[idx].message, "word"))

    def _add_ng_word(self, value, use_reg, hide, auto_ng_id, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_word(value, use_reg, hide, auto_ng_id, None, None)
        elif scope_idx == 1:
            self._data_context.add_ng_word(value, use_reg, hide, auto_ng_id, self._data_context.board, None)
        elif scope_idx == 2:
            self._data_context.add_ng_word(value, use_reg, hide, auto_ng_id,
                                           self._data_context.board, self._data_context.key)

    def _save_history(self):
        cur_bookmark = self._data_context.bookmark if self._data_context.bookmark is not None else 0
        new_bookmark = self._responses_viewer.get_last_respones_displayed()

        self._data_context.save_history(max(new_bookmark, cur_bookmark))

    def _to_bbsmenu(self):
        raise NextScene("Bbsmenu")

    def _to_board(self):
        raise NextScene("Board")

    def _to_favorites(self):
        raise NextScene("Favorites")

    def _to_ng(self):
        raise NextScene("NG")
