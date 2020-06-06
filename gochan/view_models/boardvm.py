from typing import Optional, List

from gochan.models import AppContext, Board, ThreadHeader
from gochan.event_handler import EventHandler


class BoardVM:
    def __init__(self, app_context: AppContext):
        super().__init__()

        self._app_context = app_context
        self._board = app_context.board

        self._app_context.on_property_changed = self._app_context_changed
        self.on_property_changed = EventHandler()

    @property
    def threads(self) -> Optional[List[ThreadHeader]]:
        return self._board.threads if self._board is not None else None

    def update(self):
        if self._board is not None:
            self._board.update()

    def _app_context_changed(self, property_name: str):
        if property_name == "board":
            if self._board is not None:
                self._board.on_property_changed.remove(self._board_changed)

            self._board = self._app_context.board
            self._board.on_property_changed.add(self._board_changed)

            self.on_property_changed("threads")

    def _board_changed(self, property_name):
        if property_name == "threads":
            self.on_property_changed("threads")
