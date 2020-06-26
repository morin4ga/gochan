import re
import tempfile
import pickle

from typing import Callable, List, TypeVar, Generic, Optional, Tuple
from urllib.request import HTTPError

from gochan.event_handler import EventHandler
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread
from gochan.config import USE_IMAGE_CACHE, USE_THREAD_CACHE
from gochan.storage import image_cache, thread_cache
from gochan.client import download_image
from gochan.models.ng import ng, NGList


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Bbsmenu = None
        self.board: Board = None
        self.thread: Thread = None
        self._image: Optional[str] = None
        self._image_error: Optional[HTTPError] = None
        self.ng: NGList = ng

        self.on_property_changed = EventHandler()

    @property
    def image(self) -> Optional[str]:
        return self._image

    @image.setter
    def image(self, path: str):
        self._image = path
        self.on_property_changed("image")

    @property
    def image_error(self) -> Optional[HTTPError]:
        return self._image_error

    @image_error.setter
    def image_error(self, value):
        self._image_error = value
        self.on_property_changed("image_error")

    def set_bbsmenu(self):
        self.bbsmenu = Bbsmenu()
        self.bbsmenu.update()
        self.on_property_changed("bbsmenu")

    def set_board(self, server: str, board: str):
        self.board = Board(server, board)
        self.board.update()
        self.on_property_changed("board")

    def set_thread(self, server: str, board: str, key: str):
        if USE_THREAD_CACHE:
            self.save_thread()

            if thread_cache.contains(board + "-" + key):
                data = thread_cache.get(board + "-" + key)
                d = pickle.loads(data)
                self.thread = Thread.restore(d)
                self.thread.update()
                self.on_property_changed("thread")
                return

        self.thread = Thread(server, board, key)
        self.thread.update()
        self.on_property_changed("thread")

    def save_thread(self):
        if self.thread is not None:
            data = pickle.dumps(self.thread.to_dict())
            thread_cache.store(self.thread.board + "-" + self.thread.key, data)

    def set_image(self, url: str):
        if USE_IMAGE_CACHE:
            file_name = re.sub(r'https?://|/', "", url)

            if image_cache.contains(file_name):
                self.image = image_cache.path + "/" + file_name
            else:
                result = download_image(url)

                if isinstance(result, HTTPError):
                    self.image_error = result
                else:
                    image_cache.store(file_name, result)
                    self.image = image_cache.path + "/" + file_name
        else:
            result = download_image(url)

            if isinstance(result, HTTPError):
                self.image_error = result
            else:
                f = tempfile.NamedTemporaryFile()
                f.write(result)
                self.image = f.name
                f.close()
