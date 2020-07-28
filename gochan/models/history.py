import json
from typing import Optional
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs


class ThreadHistory:
    def __init__(self, bookmark: int, retrieved_reses: int):
        super().__init__()
        self.bookmark = bookmark
        self.retrieved_reses = retrieved_reses


class History:
    def __init__(self, max_history: int):
        super().__init__()
        self._dict = {}
        self._max_history = max_history
        self.on_property_changed = PropertyChangedEventHandler()

    def get(self, board: str, key: str) -> Optional[ThreadHistory]:
        return self._dict.get(board + key)

    def save(self, board: str, key: str, bookmark: int, retrieved_reses: int):
        while self._max_history <= len(self._dict):
            self._dict.popitem()

        self._dict[board + key] = ThreadHistory(bookmark, retrieved_reses)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "self"))

    def serialize(self) -> str:
        d = {}

        for k, v in self._dict.items():
            d[k] = {"bookmark": v.bookmark, "retrieved_reses": v.retrieved_reses}

        return json.dumps(d)

    def deserialize(self, s: str):
        obj = json.loads(s)

        for k, v in obj.items():
            if len(self._dict) >= self._max_history:
                break

            self._dict[k] = ThreadHistory(v["bookmark"], v["retrieved_reses"])
