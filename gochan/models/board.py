from typing import List, Tuple


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
    def __init__(self, server: str, board: str, threads: List[ThreadHeader]):
        super().__init__()

        self.server = server
        self.board = board
        self.threads: List[ThreadHeader] = threads
