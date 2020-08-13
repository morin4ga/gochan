from typing import Union

from gochan.event_handler import (OrderChangedEventArg, OrderChangedEventHandler, PropertyChangedEventArgs,
                                  PropertyChangedEventHandler)
from gochan.models.app_context import AppContext
from gochan.models.favorites import FavoriteBoard, FavoriteThread


class FavoritesVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._app_context.favorites.on_property_changed.add(self._context_changed)
        self._app_context.favorites.on_order_changed.add(self._order_changed)

        self.on_property_changed = PropertyChangedEventHandler()
        self.on_order_changed = OrderChangedEventHandler()

    @property
    def list(self):
        return self._app_context.favorites.list

    def add(self, item: Union[FavoriteThread, FavoriteBoard]):
        self._app_context.favorites.add(item)

    def remove(self, item: Union[FavoriteThread, FavoriteBoard]):
        self._app_context.favorites.remove(item)

    def raise_order(self, item: Union[FavoriteThread, FavoriteBoard]):
        self._app_context.favorites.raise_order(item)

    def lower_order(self, item: Union[FavoriteThread, FavoriteBoard]):
        self._app_context.favorites.lower_order(item)

    def open_thread(self, item: FavoriteThread):
        self._app_context.set_thread(item.server, item.board, item.key)

    def open_board(self, item: FavoriteBoard):
        self._app_context.set_board(item.server, item.board)

    def _context_changed(self, e: PropertyChangedEventArgs):
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "list"))

    def _order_changed(self, e: OrderChangedEventArg):
        self.on_order_changed.invoke(e)
