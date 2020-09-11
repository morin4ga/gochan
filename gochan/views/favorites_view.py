from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, ListBox, Widget, Button, Divider

from gochan.event_handler import OrderChangedEventArg, PropertyChangedEventArgs
from gochan.view_models.favoritesvm import FavoritesVM, FavoriteThread
from gochan.keybinding import KEY_BINDINGS
from gochan.effects.help import Help


class FavoritesView(Frame):
    def __init__(self, screen: Screen, context: FavoritesVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         on_load=self._on_load,
                         )

        self.set_theme("user_theme")

        self._context = context
        self._context.on_property_changed.add(self._context_changed)
        self._context.on_order_changed.add(self._order_changed)

        self._list_box = ListBox(Widget.FILL_FRAME, [], on_select=self._on_select, on_change=self._on_changed)

        layout = Layout([20, 20, 20, 20, 20])
        self.add_layout(layout)
        layout.add_widget(Button("Bbsmenu", self._to_bbsmenu), 0)
        layout.add_widget(Button("Board", self._to_board), 1)
        layout.add_widget(Button("Thread", self._to_thread), 2)
        layout.add_widget(Button("Favorite", None, disabled=True), 3)
        layout.add_widget(Button("NG", self._to_ng), 4)

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_box)

        self.fix()

        self._selected_item = None
        self._list = self._context.list
        self._update_list()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == KEY_BINDINGS["global"]["help"].value:
                self._scene.add_effect(Help(self.screen))
                return None
            elif event.key_code == ord("u"):
                if self._selected_item is not None:
                    self._context.raise_order(self._selected_item)
                return None
            elif event.key_code == ord("d"):
                if self._selected_item is not None:
                    self._context.lower_order(self._selected_item)
                return None
            elif event.key_code == ord("r"):
                if self._selected_item is not None:
                    self._context.remove(self._selected_item)
                return None

        return super().process_event(event)

    def _update_list(self):
        options = []

        for i, item in enumerate(self._list):
            if isinstance(item, FavoriteThread):
                options.append((item.title, i))
            else:
                options.append((item.name, i))

        self._list_box.options = options

    def _on_load(self):
        self.switch_focus(self._layouts[2], 0, 0)

    def _on_changed(self):
        idx = self._list_box.value

        if idx is not None:
            self._selected_item = self._list[idx]

    def _on_select(self):
        if self._selected_item is not None:
            if isinstance(self._selected_item, FavoriteThread):
                self._context.open_thread(self._selected_item)
                raise NextScene("Thread")
            else:
                self._context.open_board(self._selected_item)
                raise NextScene("Board")

    def _context_changed(self, e: PropertyChangedEventArgs):
        self._list = self._context.list
        self._selected_item = None
        self._update_list()

    def _order_changed(self, e: OrderChangedEventArg):
        self._selected_item = None
        self._update_list()
        self._list_box.value = e.new_index

    def _to_bbsmenu(self):
        raise NextScene("Bbsmenu")

    def _to_board(self):
        raise NextScene("Board")

    def _to_thread(self):
        raise NextScene("Thread")

    def _to_ng(self):
        raise NextScene("NG")
