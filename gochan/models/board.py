import json
import time
from typing import List

from gochan.client import get_board
from gochan.config import NEW_THREAD_INTERVAL
from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler
from gochan.parser import BoardParser


class BreakException(Exception):
    pass


def calc_speed(key: str, count: int) -> int:
    now = int(time.time())
    since = int(key)

    diff = now - since

    if diff > 0:
        res_per_s = count / diff
        return int(res_per_s * 60 * 60 * 24)
    else:
        return 0


class ThreadHeader:
    def __init__(self, key: str, number: int, title: str, count: int, is_new: bool):
        super().__init__()
        self.key = key
        self.number = number
        self.title = title
        self.count = count
        self.is_new = is_new
        self.speed = calc_speed(key, count)


class Board:
    def __init__(self, server: str, board: str):
        super().__init__()

        self.server = server
        self.board = board
        self.threads: List[ThreadHeader] = []
        self.on_property_changed = PropertyChangedEventHandler()

    def update(self):
        s = get_board(self.server, self.board)
        parser = BoardParser(s)

        new_threads = []

        for i, t in enumerate(parser.threads(), 1):
            # If thread is new arrival
            if t["key"] not in [x.key for x in self.threads]:
                now = int(time.time())
                key = int(t["key"])

                # If the time since thread is created is less than NEW_THREAD_INTERVAL minutes from now
                if now - (NEW_THREAD_INTERVAL * 60) < key:
                    new_threads.append(ThreadHeader(t["key"], i, t["title"], t["count"], True))
                    continue

            new_threads.append(ThreadHeader(t["key"], i, t["title"], t["count"], False))

        self.threads = new_threads

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def sort_threads(self, key: str, reverse=False):
        if key == "number":
            self.threads.sort(key=lambda x: x.number, reverse=reverse)
        elif key == "title":
            self.threads.sort(key=lambda x: x.title, reverse=reverse)
        elif key == "count":
            self.threads.sort(key=lambda x: x.count, reverse=reverse)
        elif key == "unread":
            self.threads.sort(key=lambda x: x.count - x.bookmark if x.bookmark != 0 else -1, reverse=True)
        elif key == "speed":
            self.threads.sort(key=lambda x: x.speed, reverse=reverse)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def sort_threads_by_word(self, word: str):
        self.threads.sort(key=lambda x: (word not in x.title))
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def serialize(self) -> str:
        d = {}
        d["server"] = self.server
        d["board"] = self.board
        d["threads"] = []

        for t in self.threads:
            d["threads"].append({
                "number": t.number,
                "title": t.title,
                "count": t.count,
                "speed": t.speed,
                "key": t.key,
                "is_new": t.is_new
            })

        return json.dumps(d)

    @staticmethod
    def deserialize(s: str):
        obj = json.loads(s)

        b = Board(obj["server"], obj["board"])

        for t in obj["threads"]:
            b.threads.append(ThreadHeader(t["key"], t["number"], t["title"], t["count"], t["is_new"]))

        return b

    def _thread_property_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "bookmark":
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))
