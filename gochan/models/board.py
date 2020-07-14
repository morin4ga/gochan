from typing import List

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

    def sort_threads(self, key: str, reverse=False):
        if key == "number":
            self.threads.sort(key=lambda x: x.number, reverse=reverse)
        elif key == "title":
            self.threads.sort(key=lambda x: x.title, reverse=reverse)
        elif key == "count":
            self.threads.sort(key=lambda x: x.count, reverse=reverse)
        elif key == "speed":
            self.threads.sort(key=lambda x: x.speed, reverse=reverse)

        self.on_property_changed("threads")

    def sort_threads_by_word(self, word: str):
        self.threads.sort(key=lambda x: (word not in x.title))
        self.on_property_changed("threads")
