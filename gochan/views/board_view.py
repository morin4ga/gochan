from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Label, Layout, Widget

from gochan.effects.command_line import CommandLine
from gochan.effects.ng_creator import NGCreator
from gochan.effects.help import Help
from gochan.event_handler import PropertyChangedEventArgs
from gochan.keybinding import KEY_BINDINGS
from gochan.view_models.boardvm import BoardVM
from gochan.widgets.multi_col_listk import MultiColumnListBoxK


class BoardView(Frame):
    def __init__(self, screen: Screen, data_context: BoardVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         on_load=self._on_load,
                         )

        self.set_theme("user_theme")

        self._data_context: BoardVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)
        self._threads = None

        self._keybindings = KEY_BINDINGS["board"]

        self._title_label = Label("")

        self._thread_list = MultiColumnListBoxK(
            Widget.FILL_FRAME,
            ["<4%", "<70%", "<6%", "<6%", "<8", "<6"],
            [],
            self._keybindings,
            titles=["番号", "|タイトル", " |レス", " |未読", " |勢い", " |状態"],
            name="thread_list",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._on_select,
        )

        layout = Layout([20, 20, 20, 20, 20])
        self.add_layout(layout)
        layout.add_widget(Button("Bbsmenu", self._to_bbsmenu), 0)
        layout.add_widget(Button("Board", None, disabled=True), 1)
        layout.add_widget(Button("Thread", self._to_thread), 2)
        layout.add_widget(Button("Favorite", self._to_favorites), 3)
        layout.add_widget(Button("NG", self._to_ng), 4)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(self._title_label)

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._thread_list)
        layout1.add_widget(Divider())

        layout2 = Layout([25, 25, 25, 25])
        self.add_layout(layout2)
        layout2.add_widget(Button("Back", self._back_btn_clicked), 0)
        layout2.add_widget(Button("Update", self._update_btn_clicked), 1)

        self.fix()
        self._on_pick()

    def _data_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "threads":
            self._threads = self._data_context.threads
            self._update_options()
            self._update_title()
        elif e.property_name == "is_favorite":
            self._update_title()

    def _back_btn_clicked(self):
        raise NextScene("Bbsmenu")

    def _update_btn_clicked(self):
        self._data_context.update()

    def _on_load(self):
        self.switch_focus(self._layouts[3], 0, 0)

    def _on_pick(self):
        pass

    def _on_select(self):
        if self._data_context.threads is None:
            return

        self.save()
        index = self._thread_list.value
        self._data_context.set_thread(self._threads[index])
        raise NextScene("Thread")

    def _update_title(self):
        title = ""
        if self._data_context.threads is not None:
            title = self._data_context.name + " (" + str(len(self._data_context.threads)) + ")"

        if self._data_context.is_favorite:
            title += " ★"

        self._title_label.text = title

    def _update_options(self):
        if self._data_context.threads is not None:
            options = []

            for i, t in enumerate(self._data_context.threads):
                num = str(t.number)
                title = "|" + t.title
                count = " |" + str(t.count)
                unread = " |" + (str(t.unread) if t.unread is not None else "")
                speed = " |" + str(t.speed)
                state = " |"

                if t.unread is None:
                    if t.is_new:
                        state += "❕"

                elif t.unread != 0:
                    state += "➕"
                else:
                    state += "➖"

                options.append(([num, title, count, unread, speed, state], i))

            self._thread_list.options = options
        else:
            self._thread_list.options = []

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["global"]["help"].value:
                self._scene.add_effect(Help(self.screen))
                return None
            elif event.key_code == self._keybindings["num_sort"].value:
                self._data_context.sort_threads("number")
                return None
            elif event.key_code == self._keybindings["num_des_sort"].value:
                self._data_context.sort_threads("number", True)
                return None
            elif event.key_code == self._keybindings["title_sort"].value:
                self._data_context.sort_threads("title")
                return None
            elif event.key_code == self._keybindings["title_des_sort"].value:
                self._data_context.sort_threads("title", True)
                return None
            elif event.key_code == self._keybindings["count_sort"].value:
                self._data_context.sort_threads("count")
                return None
            elif event.key_code == self._keybindings["count_des_sort"].value:
                self._data_context.sort_threads("count", True)
                return None
            elif event.key_code == self._keybindings["active_sort"].value:
                self._data_context.switch_active_sort()
                return None
            elif event.key_code == self._keybindings["speed_sort"].value:
                self._data_context.sort_threads("speed")
                return None
            elif event.key_code == self._keybindings["speed_des_sort"].value:
                self._data_context.sort_threads("speed", True)
                return None
            elif event.key_code == self._keybindings["find"].value:
                self._scene.add_effect(CommandLine(self._screen, "find:", self._find))
                return None
            elif event.key_code == self._keybindings["ng_title"].value:
                self._scene.add_effect(CommandLine(self._screen, "ng:", self._open_ngcreator))
                return None
            elif event.key_code == self._keybindings["update"].value:
                self._data_context.update()
                return None
            elif event.key_code == self._keybindings["back"].value:
                raise NextScene("Bbsmenu")
                return None
            elif event.key_code == self._keybindings["favorite"].value:
                self._data_context.favorite()
                return None

        return super().process_event(event)

    def _find(self, word: str):
        if self._data_context.threads is not None:
            self._data_context.sort_threads_by_word(word)

    def _open_ngcreator(self, number: str):
        if number.isdecimal() and self._data_context.threads is not None:
            target = None
            for t in self._data_context.threads:
                if int(number) == t.number:
                    target = t
                    break

            if target is not None:
                self._scene.add_effect(NGCreator(self._screen, self._add_ng_title, target.title, "title"))

    def _add_ng_title(self, value, use_reg, scope_idx):
        if scope_idx == 0:
            self._data_context.add_ng_title(value, use_reg, None)
        elif scope_idx == 1:
            self._data_context.add_ng_title(value, use_reg, self._data_context.board)

    def _to_bbsmenu(self):
        raise NextScene("Bbsmenu")

    def _to_thread(self):
        raise NextScene("Thread")

    def _to_favorites(self):
        raise NextScene("Favorites")

    def _to_ng(self):
        raise NextScene("NG")
