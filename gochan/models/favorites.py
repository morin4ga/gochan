from typing import Union

from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs


class FavoriteThread:
    def __init__(self, title: str, server: str, board: str, key: str):
        super().__init__()
        self.title = title
        self.server = server
        self.board = board
        self.key = key


class FavoriteBoard:
    def __init__(self, name: str, server: str, board: str):
        super().__init__()
        self.name = name
        self.server = server
        self.board = board


class Favorites:
    def __init__(self):
        super().__init__()
        self.list = []
        self.on_property_changed = PropertyChangedEventHandler()

    def add(self, item: Union[FavoriteThread, FavoriteBoard]):
        self.list.append(item)
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "list"))

    def remove(self, item: Union[FavoriteThread, FavoriteBoard]):
        self.list.remove(item)
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "list"))

    def raise_order(self, item: Union[FavoriteThread, FavoriteBoard]):
        for i, x in enumerate(self.list):
            if x == item:
                if i == 0:
                    return
                else:
                    tmp = self.list[i-1]
                    self.list[i-1] = x
                    self.list[i] = tmp
                    self.on_property_changed.invoke(PropertyChangedEventArgs(self, "list"))

    def lower_order(self, item: Union[FavoriteThread, FavoriteBoard]):
        for i, x in enumerate(self.list):
            if x == item:
                if i == len(self.list) - 1:
                    return
                else:
                    tmp = self.list[i+1]
                    self.list[i+1] = x
                    self.list[i] = tmp
                    self.on_property_changed.invoke(PropertyChangedEventArgs(self, "list"))
