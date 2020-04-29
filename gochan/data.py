from typing import List, Tuple


class Response:
    def __init__(self, number: int, name: str, date: str, id: str, message: str):
        super().__init__()

        self.number = number
        self.name = name
        self.date = date
        self.id = id
        self.message = message


class Thread:
    def __init__(self, server: str, board: str, key: str, title: str, responses: List[Response]):
        super().__init__()

        self.server = server
        self.board = board
        self.key = key
        self.title = title
        self.responses = responses

    def to_text(self) -> str:
        s = ""

        for res in self.responses:
            s = s + str(res.number) + res.name + res.date + res.id + "\n\n"
            s = s + res.message + "\n\n"

        return s


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
        self.threads = threads


class BoardHeader:
    def __init__(self, server: str, board: str, name: str):
        super().__init__()

        self.server = server
        self.board = board
        self.name = name


class Category:
    def __init__(self, name: str, boards: List[BoardHeader]):
        super().__init__()

        self.name = name
        self.boards = boards

    def get_items(self) -> List[Tuple[str, int]]:
        items = []

        for i, board in enumerate(self.boards):
            items.append((board.name, i))

        return items


class Bbsmenu:
    def __init__(self, categories: List[Category]):
        super().__init__()

        self.categories = categories

    def get_items(self) -> List[Tuple[str, int]]:
        items = []

        for i, cat in enumerate(self.categories):
            items.append((cat.name, i))

        return items
