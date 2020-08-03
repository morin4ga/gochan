from asciimatics.widgets import Frame, ListBox, Widget, Layout
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from asciimatics.event import KeyboardEvent

from gochan.event_handler import PropertyChangedEventArgs, OrderChangedEventArg
from gochan.view_models.favoritesvm import FavoritesVM, FavoriteThread


class FavoritesView(Frame):
    def __init__(self, screen: Screen, context: FavoritesVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self.set_theme("user_theme")

        self._context = context
        self._context.on_property_changed.add(self._context_changed)
        self._context.on_order_changed.add(self._order_changed)

        self._list_box = ListBox(Widget.FILL_FRAME, [], on_select=self._on_select, on_change=self._on_changed)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_box)

        self.fix()

        self._selected_item = None
        self._list = self._context.list
        self._update_list()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("u"):
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
