import re
import tempfile

from typing import Optional, Union
from urllib.request import HTTPError, URLError

from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs
from gochan.models.bbsmenu import Bbsmenu
from gochan.models.board import Board
from gochan.models.thread import Thread
from gochan.config import USE_IMAGE_CACHE, SAVE_THREAD_LOG, USE_BOARD_LOG, HISTORY_PATH, MAX_HISTORY, NG_PATH
from gochan.storage import image_cache, thread_log, board_log
from gochan.models.history import History
from gochan.client import download_image
from gochan.models.ng import NG


class AppContext:
    def __init__(self):
        super().__init__()
        self.bbsmenu: Optional[Bbsmenu] = None
        self.board: Optional[Board] = None
        self.thread: Optional[Thread] = None
        self.image: Optional[Union[str, HTTPError, URLError]] = None

        self.ng: NG = NG()

        if NG_PATH.is_file():
            s = NG_PATH.read_text()

            # Ensure it's not empty
            if len(s.replace(" ", "")) != 0:
                self.ng.deserialize(s)

        self.history = History(MAX_HISTORY)

        if HISTORY_PATH.is_file():
            s = HISTORY_PATH.read_text()
            self.history.deserialize(s)

        self.on_property_changed = PropertyChangedEventHandler()

    def set_bbsmenu(self):
        self.bbsmenu = Bbsmenu()
        self.bbsmenu.update()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "bbsmenu"))

    def set_board(self, server: str, board: str):
        if USE_BOARD_LOG:
            self.save_board()

            if board_log.contains(board):
                s = board_log.get(board)
                self.board = Board.deserialize(s)
                self.board.update()
                self.on_property_changed.invoke(PropertyChangedEventArgs(self, "board"))
                return

        self.board = Board(server, board)
        self.board.update()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "board"))

    def set_thread(self, server: str, board: str, key: str):
        if SAVE_THREAD_LOG:
            self.save_thread()

            if thread_log.contains(board + key):
                s = thread_log.get(board + key)
                self.thread = Thread.deserialize(s)
                self.thread.update()
                self.on_property_changed(self, "thread")
                return

        self.thread = Thread(server, board, key)
        self.thread.update()
        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "thread"))

    def save_board(self):
        if self.board is not None:
            s = self.board.serialize()
            board_log.store(self.board.board, s.encode())

    def save_thread(self):
        if self.thread is not None:
            s = self.thread.serialize()
            thread_log.store(self.thread.board + self.thread.key, s.encode())

    def save_context(self):
        if USE_BOARD_LOG:
            self.save_board()

        if SAVE_THREAD_LOG:
            self.save_thread()

        s = self.ng.serialize()
        NG_PATH.write_text(s)

        s = self.history.serialize()
        HISTORY_PATH.write_text(s)

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

        self.on_property_changed.invoke(PropertyChangedEventArgs(self, "image"))
