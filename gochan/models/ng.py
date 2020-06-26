import re
import json

from typing import List, Dict, Union, Optional, Tuple, Any

from gochan.config import NG_PATH
from gochan.models import Response
from gochan.event_handler import EventHandler


class NGItem:
    def __init__(self, id: int, kind: str, value: str, use_reg: bool, hide: bool,
                 board: Optional[str], key: Optional[str]):
        super().__init__()
        self._id = id
        self._board = board
        self._key = key
        self._kind = kind
        self._value = value
        self._use_reg = use_reg
        self._hide = hide

    @property
    def id(self):
        return self._id

    @property
    def board(self):
        return self._board

    @property
    def key(self):
        return self._key

    @property
    def kind(self):
        return self._kind

    @property
    def value(self):
        return self._value

    @property
    def use_reg(self):
        return self._use_reg

    @property
    def hide(self):
        return self._hide

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
        self._last_id = 0

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()

    def insert(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        self._last_id += 1
        item = NGItem(self._last_id, kind, value, use_reg, hide, board, key)
        self._list.append(item)
        self._save()
        self.on_collection_changed(self, "insert", item)

    def delete(self, id: int):
        for item in self._list:
            if item.id == id:
                self._list.remove(item)
                self._save()
                self.on_collection_changed(self, "delete", item)

    def update(self, id: int, values: Dict[str, Any]):
        for item in self._list:
            if item.id == id:
                if "board" in values:
                    item._board = values["board"]
                if "key" in values:
                    item._key = values["key"]
                if "kind" in values:
                    item._kind = values["kind"]
                if "use_reg" in values:
                    item._use_reg = values["use_reg"]
                if "hide" in values:
                    item._hide = values["hide"]
                if "value" in values:
                    item._value = values["value"]

                self._save()
                self.on_collection_changed(self, "update", item)

    def select(self, kind: str):
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

    def _save(self):
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


ng = NGList()

if NG_PATH.is_file():
    text = NG_PATH.read_text()

    # Ensure it's not empty
    if len(text.replace(" ", "")) != 0:
        d = json.loads(text)

        if "items" in d:
            for item in d["items"]:
                kind = item["kind"]
                value = item["value"]

                hide = item["hide"] if "hide" in item else False
                use_reg = item["use_reg"] if "use_reg" in item else False
                board = item.get("board")
                key = item.get("key")

                ng.insert(kind, value, use_reg, hide, board, key)
