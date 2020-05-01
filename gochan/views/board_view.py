from typing import Callable, List, Tuple

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, ListBox, MultiColumnListBox, Widget

from gochan.data import Board, BoardHeader, ThreadHeader
from gochan.state import app_state


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

        self._model: Board = None

        self._thread_list = MultiColumnListBox(
            Widget.FILL_FRAME,
            ["<4%", "<82%", "<6%", "<8"],
            [],
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

    def _on_back(self):
        app_state.to_bbsmenu()

    def _on_pick(self):
        pass

    # _on_load is already used by Frame. So use _on_load_ here
    def _on_load_(self):
        if self._model == app_state.board:
            return

        self._reload_list()

    def _reload_list(self, new_value=None):
        self._model = app_state.board
        if self._model is not None:
            self._thread_list.options = [([str(x.number), "|" + x.title, " |" + str(x.count), " |" + str(x.speed)], i)
                                         for i, x in enumerate(self._model.threads)]
        else:
            self._thread_list.options = []

        self._thread_list.value = new_value

    def _on_select(self):
        self.save()
        index = self.data['thread_list']
        hdr = self._model.threads[index]
        app_state.open_thread(hdr)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Board):
        self._model = model

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                self._model.threads.sort(key=lambda x: x.number)
                self._reload_list()
                return None
            elif event.key_code == ord("Q"):
                self._model.threads.sort(key=lambda x: x.number, reverse=True)
                self._reload_list()
                return None
            elif event.key_code == ord("w"):
                self._model.threads.sort(key=lambda x: x.title)
                self._reload_list()
                return None
            elif event.key_code == ord("W"):
                self._model.threads.sort(key=lambda x: x.title, reverse=True)
                self._reload_list()
                return None
            elif event.key_code == ord("e"):
                self._model.threads.sort(key=lambda x: x.count)
                self._reload_list()
                return None
            elif event.key_code == ord("E"):
                self._model.threads.sort(key=lambda x: x.count, reverse=True)
                self._reload_list()
                return None
            elif event.key_code == ord("r"):
                self._model.threads.sort(key=lambda x: x.speed)
                self._reload_list()
                return None
            elif event.key_code == ord("R"):
                self._model.threads.sort(key=lambda x: x.speed, reverse=True)
                self._reload_list()
                return None

        return super().process_event(event)
