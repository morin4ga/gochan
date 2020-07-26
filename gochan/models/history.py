import json
from typing import Optional
from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs
from gochan.config import HISTORY_PATH, MAX_HISTORY


class ThreadHistory:
    def __init__(self, bookmark: int, retrieved_reses: int):
        super().__init__()
        self.bookmark = bookmark
        self.retrieved_reses = retrieved_reses


class History:
    def __init__(self):
        super().__init__()
        self._dict = {}
        self.on_property_changed = PropertyChangedEventHandler()

    def get(self, board: str, key: str) -> Optional[ThreadHistory]:
        return self._dict.get(board + key)

    def save(self, board: str, key: str, bookmark: int, retrieved_reses: int):
        while MAX_HISTORY <= len(self._dict):
            self._dict.popitem()

        self._dict[board + key] = ThreadHistory(bookmark, retrieved_reses)

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "self"))

    def serialize(self):
        d = {}

        for k, v in self._dict.items():
            d[k] = {"bookmark": v.bookmark, "retrieved_reses": v.retrieved_reses}

        s = json.dumps(d)
        HISTORY_PATH.write_text(s)

    def deserialize(self, d):
        for k, v in d.items():
            self._dict[k] = ThreadHistory(v["bookmark"], v["retrieved_reses"])


history = History()

if HISTORY_PATH.is_file():
    b = HISTORY_PATH.read_text()
    d = json.loads(b)
    history.deserialize(d)
