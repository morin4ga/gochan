import re
import json

from enum import Enum
from typing import List, Optional, Union

from gochan.config import NG_PATH
from gochan.event_handler import EventHandler
from gochan.models import Board, ThreadHeader, Thread, Response


class BreakException(Exception):
    pass


class NGResponse:
    def __init__(self, hide: bool, origin: Response):
        super().__init__()
        self.hide = hide
        self.origin = origin


class NGItem:
    def __init__(self, id: int, value: str, use_reg: bool):
        super().__init__()
        self.id = id
        self.value = value
        self.use_reg = use_reg

    def match(self, s) -> bool:
        if self.use_reg:
            return re.search(self.value, s) is not None
        else:
            return self.value in s


class NGName(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.board = board
        self.key = key


class NGWord(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.board = board
        self.key = key


class NGId(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.board = board
        self.key = key


class NGTitle(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, board: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.board = board


class NG:
    def __init__(self):
        super().__init__()
        self._last_id = 0
        self.names: List[NGName] = []
        self.words: List[NGWord] = []
        self.ids: List[NGId] = []
        self.titles: List[NGTitle] = []
        self.on_collection_changed = EventHandler()

    def add_ng_name(self, value: str, use_reg: bool, hide: bool,
                    board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGName(self._last_id, value, use_reg, hide, board, key)
        self.names.append(item)
        self.on_collection_changed("names", "add", item)

    def add_ng_word(self, value: str, use_reg: bool, hide: bool,
                    board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGWord(self._last_id, value, use_reg, hide, board, key)
        self.words.append(item)
        self.on_collection_changed("words", "add", item)

    def add_ng_id(self, value: str, use_reg: bool, hide: bool,
                  board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGId(self._last_id, value, use_reg, hide, board, key)
        self.ids.append(item)
        self.on_collection_changed("ids", "add", item)

    def add_ng_title(self, value: str, use_reg: bool, board: Optional[str] = None):
        self._last_id += 1
        item = NGTitle(self._last_id, value, use_reg, board)
        self.titles.append(item)
        self.on_collection_changed("titles", "add", item)

    def update_ng(self, id: int, values):
        for item in self.names:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed("names", "change", item)
                return

        for item in self.words:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed("words", "change", item)
                return

        for item in self.ids:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed("ids", "change", item)
                return

        for item in self.titles:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "board" in values:
                    item.board = values["board"]

                self.on_collection_changed("titles", "change", item)
                return

    def delete_ng(self, id: int):
        for n in self.names:
            if n.id == id:
                self.names.remove(n)
                self.on_collection_changed("names", "delete", n)
                return

        for n in self.ids:
            if n.id == id:
                self.ids.remove(n)
                self.on_collection_changed("ids", "delete", n)
                return

        for n in self.words:
            if n.id == id:
                self.words.remove(n)
                self.on_collection_changed("words", "delete", n)
                return

        for n in self.titles:
            if n.id == id:
                self.titles.remove(n)
                self.on_collection_changed("titles", "delete", n)
                return

    def filter_threads(self, board: Board) -> List[Union[ThreadHeader, None]]:
        result = []

        for h in board.threads:
            try:
                for n in self.titles:
                    # Ignore ng when the response is out of ng's scope
                    if n.board is not None and n.board != h.board:
                        continue

                    if n.match(h.title):
                        result.append(None)
                        raise BreakException()

                result.append(h)
            except BreakException:
                pass

        return result

    def filter_responses(self, thread: Thread) -> List[Union[Response, NGResponse]]:
        result = []

        for r in thread.responses:
            try:
                for n in self.names:
                    # Ignore ng when the response is out of ng's scope
                    if n.board is not None and n.board != thread.board:
                        continue
                    if n.key is not None and n.key != thread.key:
                        continue

                    if n.match(r.name):
                        result.append(NGResponse(n.hide, r))
                        raise BreakException()

                for n in self.ids:
                    # Ignore ng when the response is out of ng's scope
                    if n.board is not None and n.board != thread.board:
                        continue
                    if n.key is not None and n.key != thread.key:
                        continue

                    if n.match(r.id):
                        result.append(NGResponse(n.hide, r))
                        raise BreakException()

                for n in self.words:
                    # Ignore ng when the response is out of ng's scope
                    if n.board is not None and n.board != thread.board:
                        continue
                    if n.key is not None and n.key != thread.key:
                        continue

                    if n.match(r.message):
                        result.append(NGResponse(n.hide, r))
                        raise BreakException()

                result.append(r)

            except BreakException:
                pass

        return result

    def save(self):
        names = []
        words = []
        ids = []
        titles = []

        for name in self.names:
            d = {}
            d["value"] = name.value
            d["use_reg"] = name.use_reg
            d["hide"] = name.hide

            if name.board is not None:
                d["board"] = name.board

            if name.key is not None:
                d["key"] = name.key

            names.append(d)

        for word in self.words:
            d = {}
            d["value"] = word.value
            d["use_reg"] = word.use_reg
            d["hide"] = word.hide

            if word.board is not None:
                d["board"] = word.board

            if word.key is not None:
                d["key"] = word.key

            words.append(d)

        for id in self.ids:
            d = {}
            d["value"] = id.value
            d["use_reg"] = id.use_reg
            d["hide"] = id.hide

            if id.board is not None:
                d["board"] = id.board

            if id.key is not None:
                d["key"] = id.key

            ids.append(d)

        for title in self.titles:
            d = {}
            d["value"] = title.value
            d["use_reg"] = title.use_reg

            if title.board is not None:
                d["board"] = title.board

            titles.append(d)

        obj = {}
        obj["names"] = names
        obj["words"] = words
        obj["ids"] = ids
        obj["titles"] = titles

        j = json.dumps(obj, ensure_ascii=False, indent=2)
        NG_PATH.write_text(j)


ng = NG()

if NG_PATH.is_file():
    text = NG_PATH.read_text()

    # Ensure it's not empty
    if len(text.replace(" ", "")) != 0:
        d = json.loads(text)

        if "names" in d:
            for item in d["names"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                board = item.get("board")
                key = item.get("key")
                ng.add_ng_name(value, use_reg, hide, board, key)

        if "words" in d:
            for item in d["words"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                board = item.get("board")
                key = item.get("key")
                ng.add_ng_word(value, use_reg, hide, board, key)

        if "ids" in d:
            for item in d["ids"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                board = item.get("board")
                key = item.get("key")
                ng.add_ng_id(value, use_reg, hide, board, key)

        if "titles" in d:
            for item in d["titles"]:
                value = item["value"]
                use_reg = item["use_reg"]
                board = item.get("board")
                ng.add_ng_title(value, use_reg, board)
