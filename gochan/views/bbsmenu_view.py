from gochan.effects.help import Help
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, Widget

from gochan.event_handler import PropertyChangedEventArgs
from gochan.keybinding import KEY_BINDINGS
from gochan.view_models.bbsmenuvm import BbsmenuVM
from gochan.widgets.list_boxk import ListBoxK


class BbsmenuView(Frame):
    def __init__(self, screen: Screen, data_context: BbsmenuVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         title="Bbs Menu",
                         on_load=self._on_load)

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

        layout = Layout([20, 20, 20, 20, 20])
        self.add_layout(layout)
        layout.add_widget(Button("Bbsmenu", None, disabled=True), 0)
        layout.add_widget(Button("Board", self._to_board), 1)
        layout.add_widget(Button("Thread", self._to_thread), 2)
        layout.add_widget(Button("Favorite", self._to_favorites), 3)
        layout.add_widget(Button("NG", self._to_ng), 4)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([30, 70], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._cat_list, 0)
        layout.add_widget(self._board_list, 1)

        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["global"]["help"].value:
                self._scene.add_effect(Help(self.screen))
                return None

        return super().process_event(event)

    def _data_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "categories":
            self._update_cat_options()
        elif e.property_name == "selected_category":
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

    def _on_load(self):
        self.switch_focus(self._layouts[2], 0, 0)

    def _on_pick_c(self):
        self.save()
        index = self.data['cat_list']
        if index is not None:
            self._data_context.select_category(index)

    def _on_select_c(self):
        self.switch_focus(self._layouts[2], 1, 0)

    def _on_pick_b(self):
        pass

    def _on_select_b(self):
        self.save()
        index = self.data['board_list']

        if index is not None:
            self._data_context.select_board(index)
            raise NextScene("Board")

    def _to_board(self):
        raise NextScene("Board")

    def _to_thread(self):
        raise NextScene("Thread")

    def _to_favorites(self):
        raise NextScene("Favorites")

    def _to_ng(self):
        raise NextScene("NG")
