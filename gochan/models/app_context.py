import re
import tempfile
import pickle

from typing import Optional, Union
from urllib.request import HTTPError, URLError

from gochan.event_handler import EventHandler
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread
from gochan.config import USE_IMAGE_CACHE, SAVE_THREAD_LOG
from gochan.storage import image_cache, thread_log
from gochan.client import download_image
from gochan.models.ng import ng, NG


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Optional[Bbsmenu] = None
        self.board: Optional[Board] = None
        self.thread: Optional[Thread] = None
        self.image: Optional[Union[str, HTTPError, URLError]] = None
        self.ng: NG = ng

        self.on_property_changed = EventHandler()

    def set_bbsmenu(self):
        self.bbsmenu = Bbsmenu()
        self.bbsmenu.update()
        self.on_property_changed("bbsmenu")

    def set_board(self, server: str, board: str):
        self.board = Board(server, board)
        self.board.update()
        self.on_property_changed("board")

    def set_thread(self, server: str, board: str, key: str):
        if SAVE_THREAD_LOG:
            self.save_thread()

            if thread_log.contains(board + "-" + key):
                data = thread_log.get(board + "-" + key)
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
            thread_log.store(self.thread.board + "-" + self.thread.key, data)

    def set_image(self, url: str):
        if USE_IMAGE_CACHE:
            file_name = re.sub(r'https?://|/', "", url)

            if image_cache.contains(file_name):
                self.image = image_cache.path + "/" + file_name
            else:
                result = download_image(url)

                if isinstance(result, HTTPError) or isinstance(result, URLError):
                    self.image = result
                else:
                    image_cache.store(file_name, result)
                    self.image = image_cache.path + "/" + file_name
        else:
            result = download_image(url)

            if isinstance(result, HTTPError) or isinstance(result, URLError):
                self.image = result
            else:
                f = tempfile.NamedTemporaryFile()
                f.write(result)
                self.image = f.name
                f.close()

        self.on_property_changed("image")
