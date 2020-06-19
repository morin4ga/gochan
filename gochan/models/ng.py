import re
import json

from typing import List, Dict, Union, Optional

from gochan.config import NG_PATH
from gochan.models import Response
from gochan.event_handler import EventHandler


class NGItem:
    def __init__(self, kind: str, value: str, use_reg: bool, hide: bool,
                 board: Optional[str], key: Optional[str]):
        super().__init__()
        self._board = board
        self._key = key
        self._kind = kind
        self._value = value
        self._use_reg = use_reg
        self._hide = hide
        self.on_property_changed = EventHandler()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value: str):
        self._board = value
        self.on_property_changed(self, "board")

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value
        self.on_property_changed(self, "key")

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value: str):
        self._kind = value
        self.on_property_changed(self, "kind")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value_: str):
        self._value = value_
        self.on_property_changed(self, "value")

    @property
    def use_reg(self):
        return self._use_reg

    @use_reg.setter
    def use_reg(self, value: bool):
        self._use_reg = value
        self.on_property_changed(self, "use_reg")

    @property
    def hide(self):
        return self._hide

    @hide.setter
    def hide(self, value: bool):
        self._hide = value
        self.on_property_changed(self, "hide")

    def match(self, obj: Union[Response, str]):
        """
        Parameters
        ----------
        obj : Union[Response, str]
              Response or thread title
        """
        if isinstance(obj, Response):
            if self.kind == "name":
                if self.use_reg:
                    return re.search(self.value, obj.name) is not None
                else:
                    return self.value in obj.name
            elif self.kind == "id":
                if self.use_reg:
                    return re.search(self.value, obj.id) is not None
                else:
                    return self.value in obj.id
            elif self.kind == "word":
                if self.use_reg:
                    return re.search(self.value, obj.message) is not None
                else:
                    return self.value in obj.message

            return False
        else:
            if self.use_reg:
                return re.search(self.value, obj)
            else:
                return self.value in obj


class NGList:
    def __init__(self):
        super().__init__()
        self.on_collection_changed = EventHandler()
        self._list: List[NGItem] = []

    def __delitem__(self, key):
        item = self._list.__getitem__(key)
        item.on_property_changed.remove(self._on_item_changed)
        self._list.__delitem__(key)
        self.on_collection_changed(self, "delete", key)

    def __getitem__(self, key):
        return self._list.__getitem__(key)

    def __setitem__(self, key, value):
        self._list.__setitem__(key, value)
        self.on_collection_changed(self, "set", key)

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()

    def add_item(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        item = NGItem(kind, value, use_reg, hide, board, key)
        item.on_property_changed.add(self._on_item_changed)
        self._list.append(item)
        self.on_collection_changed(self, "add", item)

    def delete_item(self, item: NGItem):
        self._list.remove(item)
        self.on_collection_changed(self, "delete", item)

    def filter(self, kind: str):
        if kind == "title":
            return list(filter(lambda x: x.kind == "title", self._list))
        elif kind == "name":
            return list(filter(lambda x: x.kind == "name", self._list))
        elif kind == "id":
            return list(filter(lambda x: x.kind == "id", self._list))
        elif kind == "word":
            return list(filter(lambda x: x.kind == "word", self._list))
        else:
            raise ValueError("wrong kind " + kind)

    def is_ng(self, obj: Union[Response, str], board: str = None, key: str = None) -> int:
        """
        Returns
        -------
        0 : is not ng
        1 : is ng
        2 : is ng and hide
        """
        for item in self._list:
            if item.board is not None and item.board != board:
                continue
            if item.key is not None and item.key != key:
                continue

            if item.match(obj):
                return 2 if item.hide else 1

        return 0

    def save(self):
        d_list = []

        for item in self._list:
            d = {}

            if item.board is not None:
                d["board"] = item.board
            if item.key is not None:
                d["key"] = item.key

            d["kind"] = item.kind
            d["use_reg"] = item.use_reg
            d["hide"] = item.hide
            d["value"] = item.value

            d_list.append(d)

        obj = {"items": d_list}
        j = json.dumps(obj, ensure_ascii=False, indent=2)
        NG_PATH.write_text(j)

    def _on_item_changed(self, sender: NGItem, property_name: str):
        self.on_collection_changed(self, "change", self._list.index(sender))


ng = NGList()

if NG_PATH.is_file():
    d = json.loads(NG_PATH.read_text())

    for item in d["items"]:
        kind = item["kind"]
        value = item["value"]

        hide = item["hide"] if "hide" in item else False
        use_reg = item["use_reg"] if "use_reg" in item else False
        board = item.get("board")
        key = item.get("key")

        ng.add_item(kind, value, use_reg, hide, board, key)
