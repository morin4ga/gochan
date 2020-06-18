import re
import json

from typing import List, Dict, Union, Optional

from gochan.config import NG_PATH
from gochan.models import Response
from gochan.event_handler import EventHandler


class NGItem:
    def __init__(self, id: int, kind: str, value: str, use_reg: bool, hide: bool,
                 board: Optional[str], key: Optional[str]):
        super().__init__()
        self.id = id
        self.board = board
        self.key = key
        self.kind = kind
        self.value = value
        self.use_reg = use_reg
        self.hide = hide

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
        self.on_property_changed = EventHandler()
        self.list: List[NGItem] = []
        self._last_id = 0

    def add_item(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        self._last_id += 1
        self.list.append(NGItem(self._last_id, kind, value, use_reg, hide, board, key))
        self.on_property_changed("list")

    def replace_item(self, target: id, kind: str, value: str, use_reg: bool, hide: bool,
                     board: Optional[str], key: Optional[str]):
        for item in self.list:
            if item.id == target:
                self.list.remove(item)

        self.add_item(kind, value, use_reg, hide, board, key)
        self.on_property_changed("list")

    def delete_item(self, target: id):
        for item in self.list:
            if item.id == target:
                self._list.remove(item)
                self.on_property_changed("list")

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
