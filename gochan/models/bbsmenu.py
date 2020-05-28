from typing import List, Tuple


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
