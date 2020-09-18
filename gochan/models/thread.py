import json
from typing import List

from gochan.client import get_responses_after, post_response
from gochan.event_handler import (CollectionChangedEventArgs, CollectionChangedEventHandler, CollectionChangedEventKind,
                                  PropertyChangedEventArgs, PropertyChangedEventHandler)
from gochan.parser import ThreadParserH


class Response:
    def __init__(self, number: int, name: str, mail: str, date: str, id: str, message: str):
        super().__init__()

        self.number = number
        self.name = name
        self.mail = mail
        self.date = date
        self.id = id
        self.message = message


class Thread:
    def __init__(self, server: str, board: str, key: str):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.title = None
        self.responses: List[Response] = []
        self._is_pastlog: bool = False
        self.on_property_changed = PropertyChangedEventHandler()
        self.on_collection_changed = CollectionChangedEventHandler()

    @property
    def is_pastlog(self) -> bool:
        return self._is_pastlog

    @is_pastlog.setter
    def is_pastlog(self, value: bool):
        self._is_pastlog = value
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))

    def serialize(self) -> str:
        d = {}
        d["server"] = self.server
        d["board"] = self.board
        d["key"] = self.key
        d["title"] = self.title
        d["is_pastlog"] = self.is_pastlog
        d["responses"] = []

        for r in self.responses:
            d2 = {}
            d2["number"] = r.number
            d2["name"] = r.name
            d2["mail"] = r.mail
            d2["date"] = r.date
            d2["id"] = r.id
            d2["message"] = r.message

            d["responses"].append(d2)

        return json.dumps(d, ensure_ascii=False)

    @staticmethod
    def deserialize(s: str) -> "Thread":
        d = json.loads(s)

        t = Thread(d["server"], d["board"], d["key"])
        t.title = d["title"]
        t.is_pastlog = d["is_pastlog"]

        for r in d["responses"]:
            t.responses.append(Response(r["number"], r["name"], r["mail"], r["date"], r["id"], r["message"]))

        return t

    def init(self):
        html = get_responses_after(self.server, self.board, self.key, len(self.responses))
        parser = ThreadParserH(html)

        self.is_pastlog = parser.is_pastlog()

        if self.title is None:
            self.title = parser.title()

        for r in parser.responses():
            self.responses.append(Response(r["number"], r["name"], r["mail"], r["date"], r["id"], r["message"]))

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "title"))

        self.on_collection_changed.invoke(CollectionChangedEventArgs(
            self, "responses", CollectionChangedEventKind.EXTEND, self.responses[0:]))

    def update(self):
        html = get_responses_after(self.server, self.board, self.key, len(self.responses))
        parser = ThreadParserH(html)

        self.is_pastlog = parser.is_pastlog()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "is_pastlog"))

        new_responses = []
        for r in parser.responses():
            new_responses.append(Response(r["number"], r["name"], r["mail"], r["date"], r["id"], r["message"]))

        last_count = len(self.responses)

        # There are no new posts
        if len(new_responses) == 1:
            return

        self.responses.extend(new_responses[1:])

        self.on_collection_changed.invoke(CollectionChangedEventArgs(
            self, "responses", CollectionChangedEventKind.EXTEND, self.responses[last_count:]))

    def post(self, name: str, mail: str, message: str) -> str:
        return post_response(self.server, self.board, self.key, name, mail, message)
