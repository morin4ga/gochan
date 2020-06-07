from typing import List, Tuple

from gochan.client import get_bbsmenu
from gochan.event_handler import EventHandler
from gochan.parser import BbsmenuParser


class BoardHeader:
    def __init__(self, server: str, board: str, name: str):
        super().__init__()

        self.server = server
        self.board = board
        self.name = name


class Category:
    def __init__(self, name: str, boards: List[BoardHeader]):
        super().__init__()

        self.name: str = name
        self.boards: List[BoardHeader] = boards


class Bbsmenu:
    def __init__(self):
        super().__init__()

        self.categories = None
        self.on_property_changed = EventHandler()

    def update(self):
        html = get_bbsmenu()
        parser = BbsmenuParser(html)
        self.categories = []

        for c in parser.categories():
            boards = []
            for b in c["boards"]:
                boards.append(BoardHeader(b["server"], b["board"], b["name"]))

            self.categories.append(Category(c["name"], boards))

        self.on_property_changed("categories")
