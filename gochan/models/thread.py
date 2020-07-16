import re
import time

from typing import List, Dict, Union

from gochan.client import get_responses_after, post_response
from gochan.parser import ThreadParserH
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs, CollectionChangedEventHandler, \
    CollectionChangedEventArgs, CollectionChangedEventKind


class Response:
    def __init__(self, number: int, name: str, mail: str, date: str, id: str, message: str):
        super().__init__()

        self.number = number
        self.name = name
        self.mail = mail
        self.date = date
        self.id = id
        self.message = message

    @staticmethod
    def restore(dict) -> "Response":
        return Response(dict["number"], dict["name"], dict["mail"], dict["date"], dict["id"], dict["message"])

    def to_dict(self):
        d = {}
        d["number"] = self.number
        d["name"] = self.name
        d["mail"] = self.mail
        d["date"] = self.date
        d["id"] = self.id
        d["message"] = self.message

        return d


class Thread:
    def __init__(self, server: str, board: str, key: str,
                 number: int = 0, title: str = None, count: int = 0):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.number = number
        self.title = title
        self._count = count
        self._speed = calc_speed(key, count)
        self.responses: List[Response] = []
        self._is_pastlog: bool = False
        self.links = []
        self._bookmark = 0
        self.on_property_changed = PropertyChangedEventHandler()
        self.on_collection_changed = CollectionChangedEventHandler()

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int):
        self._count = value
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "count"))
        self._speed = calc_speed(self.key, self.count)
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "speed"))

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def is_pastlog(self) -> bool:
        return self._is_pastlog

    @is_pastlog.setter
    def is_pastlog(self, value: bool):
        self._is_pastlog = value
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))

    @property
    def bookmark(self) -> int:
        return self._bookmark

    @bookmark.setter
    def bookmark(self, value: int):
        self._bookmark = value
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "bookmark"))

    @staticmethod
    def restore(dict) -> "Thread":
        t = Thread(dict["server"], dict["board"], dict["key"])
        t.title = dict["title"]
        t.links = dict["links"]
        t.is_pastlog = dict["is_pastlog"]
        t.bookmark = dict["bookmark"]
        t.responses = []

        for r in dict["responses"]:
            t.responses.append(Response.restore(r))

        return t

    def update(self):
        html = get_responses_after(self.server, self.board, self.key, len(self.responses))
        parser = ThreadParserH(html)

        self.is_pastlog = parser.is_pastlog()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))

        if self.title is None:
            self.title = parser.title()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "title"))

        # If responses has not initialtzed yet
        if len(self.responses) == 0:
            self._add_response(parser.responses())
            self.on_collection_changed.invoke(CollectionChangedEventArgs(
                self, "responses", CollectionChangedEventKind.EXTEND, self.responses[0:]))
        else:
            # Add new responses
            rs = parser.responses()

            if len(rs) > 1:
                start = len(self.responses)
                self._add_response(rs[1:])
                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "responses", CollectionChangedEventKind.EXTEND, self.responses[start:]))

        self.count = len(self.responses)

    def post(self, name: str, mail: str, message: str) -> str:
        return post_response(self.server, self.board, self.key, name, mail, message)

    def to_dict(self):
        d = {}
        d["server"] = self.server
        d["board"] = self.board
        d["key"] = self.key
        d["title"] = self.title
        d["is_pastlog"] = self.is_pastlog
        d["links"] = self.links
        d["bookmark"] = self.bookmark
        d["responses"] = []

        for r in self.responses:
            d["responses"].append(r.to_dict())

        return d

    def _add_response(self, rs: List[Dict[str, Union[int, str]]]):
        for r in rs:
            self.responses.append(Response(r["num"], r["name"], r["mail"], r["date"], r["id"], r["msg"]))

            for link in re.finditer(r'(https?://.*?)(?=$|\n| )', r["msg"]):
                self.links.append(link.group(1))


def calc_speed(key: str, count: int) -> int:
    now = int(time.time())
    since = int(key)

    diff = now - since

    if diff > 0:
        res_per_s = count / diff
        return int(res_per_s * 60 * 60 * 24)
    else:
        return 0
