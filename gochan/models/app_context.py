import re
import tempfile

from typing import Callable, List, TypeVar, Generic, Optional, Tuple
from urllib.request import HTTPError

from gochan.event_handler import EventHandler
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread
from gochan.config import USE_CACHE
from gochan.storage import storage
from gochan.client import download_image


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Bbsmenu = None
        self.board: Board = None
        self.thread: Thread = None
        self._image: Optional[str] = None
        self._image_error: Optional[HTTPError] = None

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
        self.thread = Thread(server, board, key)
        self.thread.update()
        self.on_property_changed("thread")

    def set_image(self, url: str):
        if USE_CACHE:
            file_name = re.sub(r'https?://|/', "", url)

            cache = storage.get_cache(file_name)
            if cache is not None:
                self.image = cache
            else:
                result = download_image(url)

                if isinstance(result, HTTPError):
                    self.image_error = result
                else:
                    path = storage.store_cache(file_name, result)
                    self.image = path
        else:
            result = download_image(url)

            if isinstance(result, HTTPError):
                self.image_error = result
            else:
                f = tempfile.NamedTemporaryFile()
                f.write(result)
                self.image = f.name
                f.close()
