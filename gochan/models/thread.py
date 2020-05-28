from typing import List


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

    def add_responses(self, responses: List[Response]):
        self.responses.extend(responses)
