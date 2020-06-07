import re
import tempfile

from typing import TYPE_CHEKING, Callable, List, TypeVar, Generic, Optional

from gochan.event_handler import EventHandler
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread
from gochan.config import USE_CACHE
from gochan.storage import storage
from gochan.browser import download_image


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Bbsmenu = None
        self.board: Board = None
        self.thread: Thread = None
        self._image: Optional[str] = None

        self.on_property_changed = EventHandler()

    @property
    def image(self) -> Optional[str]:
        return self._image

    @image.setter
    def image(self, path: str):
        self._image = path
        self.on_property_changed("image")

    def set_bbsmenu(self):
        self.bbsmenu = Bbsmenu.get_bbsmenu()
        self.on_property_changed("bbsmenu")

    def set_board(self, server: str, board: str):
        self.board = Board.get_board(server, board)
        self.on_property_changed("board")

    def set_thread(self, server: str, board: str, key: str):
        self.thread = Thread.get_thread(server, board, key)
        self.on_property_changed("thread")

    def set_image(self, url: str):
        if USE_CACHE:
            file_name = re.sub(r'https?://|/', "", url)

            cache = storage.get_cache(file_name)
            if cache is not None:
                self.image = cache
            else:
                data = download_image(url)
                path = storage.store_cache(file_name, data)
                self.image = path
        else:
            data = download_image(url)
            f = tempfile.NamedTemporaryFile()
            f.write(data)
            self.image = f.name
            f.close()
