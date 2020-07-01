import re
import time
import urllib
from pathlib import Path, PosixPath
from typing import Optional

from gochan.config import CACHE_PATH, MAX_IMAGE_CACHE, LOG_PATH, MAX_THREAD_LOG


class Storage:
    def __init__(self, path: Path, max_cache: int):
        super().__init__()
        self._path: Path = path
        self._max_cache = max_cache

    @property
    def path(self):
        return str(self._path)

    def contains(self, file_name) -> bool:
        return self._path.joinpath(file_name).exists()

    def get(self, file_name) -> bytes:
        return self._path.joinpath(file_name).read_bytes()

    def store(self, file_name, data):
        if not self._path.exists():
            self._path.mkdir(mode=0o777, parents=True)

        dst = self._path.joinpath(file_name)
        dst.write_bytes(data)

        # remove overflowed file
        items = list(self._path.iterdir())
        items.sort(key=lambda x: x.stat().st_atime)

        for i in range((len(items) + 1) - self._max_cache):
            items[i].unlink()


image_cache = Storage(CACHE_PATH, MAX_IMAGE_CACHE)
thread_log = Storage(LOG_PATH, MAX_THREAD_LOG)
