import re
import json

from typing import List, Dict, Union

from gochan.config import NG_PATH
from gochan.models import Response


class NGItem:
    def __init__(self, kind: str, value: str, use_reg: bool, hide: bool, board: str = None, key: str = None):
        super().__init__()
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
        self.list: List[NGItem] = []

    def is_ng(self, obj: Union[Response, str], board: str = None, key: str = None) -> int:
        """
        Returns
        -------
        0 : is not ng
        1 : is ng
        2 : is ng and hide
        """
        for item in self.list:
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

        ng.list.append(NGItem(kind, value, use_reg, hide, board, key))
