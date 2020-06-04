from typing import List

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


class Thread:
    def __init__(self, server: str, board: str, key: str, title: str, responses: List[Response], is_pastlog: bool):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.title: str = title
        self.responses: List[Response] = responses
        self.is_pastlog: bool = is_pastlog
        self.on_property_changed = EventHandler()
        self.on_collection_changed = EventHandler()

    def update(self):
        html = get_responses_after(len(self.responses))
        parser = ThreadParserH(html, self.server, self.board, self.key)

        rs = parser.responses()[1:]
        self.responses.extend(rs)
        self.on_collection_changed("responses", rs)

        self.is_pastlog = parser.is_pastlog()
        self.on_property_changed("is_pastlog")

    def post(self, name: str, mail: str, message: str):
        post_response(self.server, self.board, self.key, name, mail, message)

    @staticmethod
    def get_thread(server: str, board: str, key: str):
        html = get_thread_h(server, board, key)
        parser = ThreadParserH(html, server, board, key)
        return parser.thread()
