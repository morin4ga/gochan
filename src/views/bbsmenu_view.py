from asciimatics.widgets import Frame, ListBox, Layout, Widget
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from data import Bbsmenu, BoardHeader
from typing import Callable
from style import style


class BbsmenuView(Frame):
    def __init__(self, screen: Screen, model: Bbsmenu):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._reload_list,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         title="Bbs Menu",
                         )

        self.palette["background"] = style.normal
        self.palette["button"] = style.normal
        self.palette["borders"] = style.normal
        self.palette["field"] = style.normal
        self.palette["focus_field"] = style.normal

        self._model = model
        self.on_board_selected = None

        self._cat_list = ListBox(
            Widget.FILL_COLUMN,
            model.get_items(),
            name="cat_list",
            add_scroll_bar=True,
            on_change=self._on_pick_c,
            on_select=self._on_select_c,
        )

        self._board_list = ListBox(
            Widget.FILL_COLUMN,
            [],
            name="board_list",
            add_scroll_bar=True,
            on_change=self._on_pick_b,
            on_select=self._on_select_b,
        )

        layout = Layout([30, 70], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._cat_list, 0)
        layout.add_widget(self._board_list, 1)

        self.fix()

    def _reload_list(self, new_value=None):
        self._cat_list.options = self._model.get_items()
        self._cat_list.value = new_value
        self._on_pick_c()

    def _on_pick_c(self):
        self.save()

        if "cat_list" in self.data:
            index = self.data['cat_list']
            if index is not None:
                self._board_list.options = self._model.categories[index].get_items()

    def _on_select_c(self):
        self.save()
        index = self.data['cat_list']
        self._board_list.options = self._model.categories[index].get_items()
        self.switch_focus(self._layouts[0], 1, 0)

    def _on_pick_b(self):
        pass

    def _on_select_b(self):
        self.save()
        index1 = self.data['cat_list']
        index2 = self.data['board_list']
        board_hdr = self._model.categories[index1].boards[index2]
        self.on_board_selected(board_hdr)
