import re
import time
import urllib
from pathlib import Path, PosixPath

from gochan.config import CACHE_PATH, MAX_CACHE


class Storage:
    def __init__(self, path: str, max_cache: int):
        super().__init__()
        self._dir = Path(path).expanduser()
        self._max_cache = max_cache

    def get_cache(self, file_name) -> str:
        if not self._dir.exists():
            self._dir.mkdir(mode=0o777, parents=True)

        for item in self._dir.iterdir():
            if file_name == item.name:
                return self._dir.joinpath(item.name)

        return None

    def store_cache(self, file_name, data) -> str:
        if not self._dir.exists():
            self._dir.mkdir(mode=0o777, parents=True)

        dst = self._dir.joinpath(file_name)

        items = list(self._dir.iterdir())
        items.sort(key=lambda x: x.stat().st_atime)

        for i in range((len(items) + 1) - self._max_cache):
            items[i].unlink()

        dst.write_bytes(data)
        return str(dst)


storage = Storage(CACHE_PATH, MAX_CACHE)
