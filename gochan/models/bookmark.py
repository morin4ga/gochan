from typing import Optional

from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs


class Bookmark:
    def __init__(self):
        super().__init__()
        self._dict = {}
        self._max_bookmark = 100
        self.on_property_changed = PropertyChangedEventHandler()

    def get(self, board: str, key: str) -> Optional[int]:
        return self._dict.get(board + key)

    def save(self, board: str, key: str, position: int):
        while self._max_bookmark <= len(self._dict):
            self._dict.popitem()

        self._dict[board + key] = position

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "self"))
