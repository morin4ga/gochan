from typing import Callable, Dict, List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, ListBox, MultiColumnListBox, Widget

from gochan.config import KEY_BINDINGS
from gochan.controller import controller
from gochan.view_models import BoardVM
from gochan.effects import CommandLine
from gochan.widgets import MultiColumnListBoxK


class BoardView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self.set_theme("user_theme")

        self._data_context: BoardVM = None

        self._keybindings = KEY_BINDINGS["board"]

        self._cli = None

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

        self._back_button = Button("Back", self._on_back)

        layout1 = Layout([100], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._thread_list)
        layout1.add_widget(Divider())

        layout2 = Layout([25, 25, 25, 25])
        self.add_layout(layout2)
        layout2.add_widget(self._back_button, 0)

        self.fix()
        self._on_pick()

    def bind(self, context: BoardVM):
        self._data_context = context
        self._data_context.on_property_changed.add()

        self._update_options()

    def _data_context_changed(self, property_name: str):
        if property_name == "threads":
            self._update_options()

    def _on_back(self):
        raise NextScene(controller.bbsmenu.scene_name)

    def _on_pick(self):
        pass

    # _on_load is already used by Frame. So use _on_load_ here
    def _on_load_(self, new_value=None):
        self._thread_list.value = new_value

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
                                         for i, x in enumerate(self._data_context.threads)]
        else:
            self._thread_list.options = []

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == self._keybindings["sort_1"]:
                if self._cli is None:
                    self._data_context.sort_thread("number")
                    return None
            elif event.key_code == self._keybindings["dsort_1"]:
                if self._cli is None:
                    self._data_context.sort_thread("number", True)
                    return None
            elif event.key_code == self._keybindings["sort_2"]:
                if self._cli is None:
                    self._data_context.sort_thread("title")
                    return None
            elif event.key_code == self._keybindings["dsort_2"]:
                if self._cli is None:
                    self._data_context.sort_thread("title", True)
                    return None
            elif event.key_code == self._keybindings["sort_3"]:
                if self._cli is None:
                    self._data_context.sort_thread("count")
                    return None
            elif event.key_code == self._keybindings["dsort_3"]:
                if self._cli is None:
                    self._data_context.sort_thread("count", True)
                    return None
            elif event.key_code == self._keybindings["sort_4"]:
                if self._cli is None:
                    self._data_context.sort_thread("speed")
                    return None
            elif event.key_code == self._keybindings["dsort_4"]:
                if self._cli is None:
                    self._data_context.sort_thread("speed", True)
                    return None
            elif event.key_code == ord("f"):
                if self._cli is None:
                    self._cli = CommandLine(self._screen, "find:", self._find)
                    self._scene.add_effect(self._cli)
                    return None

        return super().process_event(event)

    def _find(self, word: str):
        if self._data_context.threads is not None:
            self._data_context.threads.sort(key=lambda x: (word not in x.title, self._sort_key(x)))
            self._update_options()
            self._cli = None
