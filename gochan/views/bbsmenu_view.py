from typing import Callable, Optional

from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Widget

from gochan.config import KEY_BINDINGS
from gochan.view_models import BbsmenuVM
from gochan.widgets import ListBoxK


class BbsmenuView(Frame):
    def __init__(self, screen: Screen, data_context: BbsmenuVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         title="Bbs Menu",
                         )

        self.set_theme("user_theme")

        self._data_context: BbsmenuVM = data_context
        self._data_context.on_property_changed.add(self._data_context_changed)

        self._keybindings = KEY_BINDINGS["bbsmenu"]

        self._cat_list = ListBoxK(
            Widget.FILL_COLUMN,
            [],
            self._keybindings,
            name="cat_list",
            add_scroll_bar=True,
            on_change=self._on_pick_c,
            on_select=self._on_select_c,
        )

        self._board_list = ListBoxK(
            Widget.FILL_COLUMN,
            [],
            self._keybindings,
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

    def _data_context_changed(self, property_name: str):
        if property_name == "categories":
            self._update_cat_options()
        elif property_name == "selected_category":
            self._update_board_options()

    def _update_cat_options(self):
        if self._data_context.categories is not None:
            options = []
            for i, c in enumerate(self._data_context.categories):
                options.append((c.name, i))

            self._cat_list.options = options

    def _update_board_options(self):
        if self._data_context.selected_category is not None:
            opitons = []
            for i, b in enumerate(self._data_context.selected_category.boards):
                opitons.append((b.name, i))

            self._board_list.options = opitons

    def _on_load_(self, new_value=None):
        self._cat_list.value = new_value
        self._on_pick_c()

    def _on_pick_c(self):
        self.save()
        index = self.data['cat_list']
        if index is not None:
            self._data_context.select_category(index)

    def _on_select_c(self):
        self.switch_focus(self._layouts[0], 1, 0)

    def _on_pick_b(self):
        pass

    def _on_select_b(self):
        self.save()
        index = self.data['board_list']

        if index is not None:
            self._data_context.select_board(index)
            raise NextScene("Board")
