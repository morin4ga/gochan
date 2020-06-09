import re

from typing import List, Dict, Union

from gochan.client import get_thread_h, get_responses_after, post_response
from gochan.parser import ThreadParserH
from gochan.event_handler import EventHandler


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
    def __init__(self, server: str, board: str, key: str):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.title: str = None
        self.responses: List[Response] = None
        self.is_pastlog: bool = False
        self.links = []
        self.on_property_changed = EventHandler()
        self.on_collection_changed = EventHandler()

    @staticmethod
    def restore(dict) -> "Thread":
        t = Thread(dict["server"], dict["board"], dict["key"])
        t.title = dict["title"]
        t.links = dict["links"]
        t.is_pastlog = dict["is_pastlog"]
        t.responses = []

        for r in dict["responses"]:
            t.responses.append(Response.restore(r))

        return t

    def update(self):
        # If this instance has not initialized yet
        if self.responses is None:
            html = get_thread_h(self.server, self.board, self.key)
            parser = ThreadParserH(html)

            self.title = parser.title()
            self.on_property_changed("title")
            self.is_pastlog = parser.is_pastlog()
            self.on_property_changed("is_pastlog")

            self.responses = []
            self._add_response(parser.responses())
            self.on_collection_changed(("responses", "add", self.responses[0:]))
        else:
            html = get_responses_after(self.server, self.board, self.key, len(self.responses))
            parser = ThreadParserH(html)

            new = parser.responses()

            if len(new) > 1:
                start = len(self.responses)
                self._add_response(new[1:])
                self.on_collection_changed(("responses", "add", self.responses[start:]))

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
        d["responses"] = []

        for r in self.responses:
            d["responses"].append(r.to_dict())

        return d

    def _add_response(self, rs: List[Dict[str, Union[int, str]]]):
        for r in rs:
            self.responses.append(Response(r["num"], r["name"], r["mail"], r["date"], r["id"], r["msg"]))

            for link in re.finditer(r'(https?://.*?)(?=$|\n| )', r["msg"]):
                self.links.append(link.group(1))
