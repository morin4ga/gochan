import pickle
from typing import List

from gochan.client import get_board
from gochan.parser import BoardParser
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs
from gochan.models.thread import Thread
from gochan.storage import thread_log
from gochan.config import SAVE_THREAD_LOG


class BreakException(Exception):
    pass


class Board:
    def __init__(self, server: str, board: str):
        super().__init__()

        self.server = server
        self.board = board
        self.threads: List[Thread] = []
        self.on_property_changed = PropertyChangedEventHandler()

    def update(self):
        s = get_board(self.server, self.board)
        parser = BoardParser(s)

        new_threads = []

        for i, t in enumerate(parser.threads(), 1):
            try:
                # If the thread is exist, reuse the instance
                for thread in self.threads:
                    if t["key"] == thread.key:
                        thread.count = t["count"]
                        thread.number = i
                        new_threads.append(thread)
                        self.threads.remove(thread)
                        raise BreakException()

                if SAVE_THREAD_LOG and thread_log.contains(self.board + "-" + t["key"]):
                    data = thread_log.get(self.board + "-" + t["key"])
                    d = pickle.loads(data)
                    thread = Thread.restore(d)
                    thread.count = t["count"]
                    thread.number = i
                    new_threads.append(thread)
                    raise BreakException()

                new_thread = Thread(self.server, self.board, t["key"],
                                    i, t["title"], t["count"])
                new_thread.on_property_changed.add(self._thread_property_changed)
                new_threads.append(new_thread)
            except BreakException:
                pass

        # Remove event from threads disappeared from board
        for lost_thread in self.threads:
            lost_thread.on_property_changed.remove(self._thread_property_changed)

        self.threads = new_threads
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def sort_threads(self, key: str, reverse=False):
        if key == "number":
            self.threads.sort(key=lambda x: x.number, reverse=reverse)
        elif key == "title":
            self.threads.sort(key=lambda x: x.title, reverse=reverse)
        elif key == "count":
            self.threads.sort(key=lambda x: x.count, reverse=reverse)
        elif key == "speed":
            self.threads.sort(key=lambda x: x.speed, reverse=reverse)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def sort_threads_by_word(self, word: str):
        self.threads.sort(key=lambda x: (word not in x.title))
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))

    def _thread_property_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "bookmark":
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "threads"))
