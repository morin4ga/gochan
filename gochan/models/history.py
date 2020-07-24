from typing import Optional
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs


class ThreadHistory:
    def __init__(self, bookmark: int, acquired_reses: int):
        super().__init__()
        self.bookmark = bookmark
        self.acquired_reses = acquired_reses


class History:
    def __init__(self):
        super().__init__()
        self._dict = {}
        self._max_history = 100
        self.on_property_changed = PropertyChangedEventHandler()

    def get(self, board: str, key: str) -> Optional[ThreadHistory]:
        return self._dict.get(board + key)

    def save(self, board: str, key: str, bookmark: int, acquired_reses: int):
        while self._max_history <= len(self._dict):
            self._dict.popitem()

        self._dict[board + key] = ThreadHistory(bookmark, acquired_reses)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "self"))
