from typing import Callable, Dict, List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, ListBox, MultiColumnListBox, Widget, Label

from gochan.config import KEY_BINDINGS
from gochan.view_models import BoardVM
from gochan.effects import CommandLine, NGCreator
from gochan.widgets import MultiColumnListBoxK


class BoardView(Frame):
    def __init__(self, screen: Screen, data_context: BoardVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self.set_theme("user_theme")

        self._data_context: BoardVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)

        self._keybindings = KEY_BINDINGS["board"]

        self._title_label = Label("")

        self._thread_list = MultiColumnListBoxK(
            Widget.FILL_FRAME,
            ["<4%", "<82%", "<6%", "<8"],
            [],
            self._keybindings,
            titles=["番号", "|タイトル", " |レス", " |勢い"],
            name="thread_list",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._on_select,
        )

        l = Layout([100])
        self.add_layout(l)
        l.add_widget(self._title_label)

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

    def _data_context_changed(self, property_name: str):
        if property_name == "threads":
            self._update_options()
            self._title_label.text = self._data_context.name + "(" + str(len(self._data_context.threads)) + ")"
        elif property_name == "ng":
            self._update_options()

    def _back_btn_clicked(self):
        raise NextScene("Bbsmenu")

    def _update_btn_clicked(self):
        self._data_context.update()

    def _on_pick(self):
        pass

    def _on_select(self):
        if self._data_context.threads is None:
            return

        self.save()
        index = self.data['thread_list']
        self._data_context.select_thread(index)
        raise NextScene("Thread")

    def _update_options(self):
        if self._data_context.threads is not None:
            self._thread_list.options = [([str(x.number), "|" + x.title, " |" + str(x.count), " |" + str(x.speed)], i)
                                         for i, x in enumerate(self._data_context.threads)
                                         if self._data_context.ng.is_ng(x.title, self._data_context.board) == 0]
        else:
            self._thread_list.options = []

    def process_event(self, event):
        if isinstance(event, KeyboardEvent) and len(self._scene.effects) == 1:
            if event.key_code == self._keybindings["sort_1"]:
                self._data_context.sort_thread("number")
                return None
            elif event.key_code == self._keybindings["dsort_1"]:
                self._data_context.sort_thread("number", True)
                return None
            elif event.key_code == self._keybindings["sort_2"]:
                self._data_context.sort_thread("title")
                return None
            elif event.key_code == self._keybindings["dsort_2"]:
                self._data_context.sort_thread("title", True)
                return None
            elif event.key_code == self._keybindings["sort_3"]:
                self._data_context.sort_thread("count")
                return None
            elif event.key_code == self._keybindings["dsort_3"]:
                self._data_context.sort_thread("count", True)
                return None
            elif event.key_code == self._keybindings["sort_4"]:
                self._data_context.sort_thread("speed")
                return None
            elif event.key_code == self._keybindings["dsort_4"]:
                self._data_context.sort_thread("speed", True)
                return None
            elif event.key_code == ord("f"):
                self._scene.add_effect(CommandLine(self._screen, "find:", self._find))
                return None
            elif event.key_code == ord("n"):
                self._scene.add_effect(CommandLine(self._screen, "ng:", self._add_ng))
                return None

        return super().process_event(event)

    def _find(self, word: str):
        if self._data_context.threads is not None:
            self._data_context.sort_thread_by_word(word)

    def _add_ng(self, number: str):
        if number.isdecimal() and self._data_context.threads is not None:
            target = None
            for t in self._data_context.threads:
                if int(number) == t.number:
                    target = t
                    break

            if target is not None:
                self._scene.add_effect(NGCreator(self._screen, self._data_context.add_ng, "title",
                                                 target.title, self._data_context.board))
