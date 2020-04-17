from asciimatics.widgets import Frame, ListBox, Layout, Widget
from asciimatics.screen import Screen
from data import Board, BoardHeader, ThreadHeader
from typing import Callable


class BoardView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._reload_list,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self._model: Board = None
        self.on_thread_selected: Callable[[ThreadHeader], None] = None

        self._thread_list = ListBox(
            Widget.FILL_FRAME,
            [],
            name="thread_list",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._on_select,
        )

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._thread_list)

        self.fix()
        self._on_pick()

    def _on_pick(self):
        pass

    def _reload_list(self, new_value=None):
        if self._model is not None:
            self._thread_list.options = self._model.get_items()

        self._thread_list.value = new_value

    def _on_select(self):
        self.save()
        index = self.data['thread_list']
        hdr = self._model.threads[index]
        self.on_thread_selected(hdr)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Board):
        self._model = model
        self._thread_list.options = model.get_items()
