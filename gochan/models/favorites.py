import json
from typing import Union

from gochan.event_handler import (OrderChangedEventArg, OrderChangedEventHandler, PropertyChangedEventArgs,
                                  PropertyChangedEventHandler)


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
        self.on_order_changed = OrderChangedEventHandler()

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
                    self.on_order_changed.invoke(OrderChangedEventArg(self, "list", x, i-1))
                    return

    def lower_order(self, item: Union[FavoriteThread, FavoriteBoard]):
        for i, x in enumerate(self.list):
            if x == item:
                if i == len(self.list) - 1:
                    return
                else:
                    tmp = self.list[i+1]
                    self.list[i+1] = x
                    self.list[i] = tmp
                    self.on_order_changed.invoke(OrderChangedEventArg(self, "list", x, i+1))
                    return

    def serialzie(self) -> str:
        d = {"items": []}

        for item in self.list:
            if isinstance(item, FavoriteThread):
                d["items"].append({"title": item.title, "server": item.server, "board": item.board, "key": item.key})
            else:
                d["items"].append({"name": item.name, "server": item.server, "board": item.board})

        return json.dumps(d)

    def deserialize(self, s: str):
        d = json.loads(s)

        for item in d["items"]:
            if "title" in item:
                self.list.append(FavoriteThread(item["title"], item["server"], item["board"], item["key"]))
            else:
                self.list.append(FavoriteBoard(item["name"], item["server"], item["board"]))
