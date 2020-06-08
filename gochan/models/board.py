from typing import List, Tuple

from gochan.client import get_board
from gochan.parser import BoardParser
from gochan.event_handler import EventHandler


class ThreadHeader:
    def __init__(self, server: str, board: str, key: str, number: int, title: str, count: int, speed: int):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.number = number
        self.title = title
        self.count = count
        self.speed = speed


class Board:
    def __init__(self, server: str, board: str):
        super().__init__()

        self.server = server
        self.board = board
        self.threads: List[ThreadHeader] = None
        self.on_property_changed = EventHandler()

    def update(self):
        s = get_board(self.server, self.board)
        parser = BoardParser(s)

        self.threads = []

        for i, t in enumerate(parser.threads(), 1):
            self.threads.append(ThreadHeader(self.server, self.board, t["key"],
                                             i, t["title"], t["count"], t["speed"]))

        self.on_property_changed("threads")
