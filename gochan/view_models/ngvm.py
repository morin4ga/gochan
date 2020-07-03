from typing import Optional, Any, Dict
from gochan.models import AppContext
from gochan.event_handler import EventHandler


class NGVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = EventHandler()

        self.title_ngs = self._app_context.ng.select("title")
        self.name_ngs = self._app_context.ng.select("name")
        self.id_ngs = self._app_context.ng.select("id")
        self.word_ngs = self._app_context.ng.select("word")

    def insert(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        self._app_context.ng.insert(kind, value, use_reg, hide, board, key)

    def update(self, target: id, values: Dict[str, Any]):
        self._app_context.ng.update(target, values)

    def delete(self, target: id):
        self._app_context.ng.delete(target)

    def _ng_changed(self, property_name: str, type: str, *arg):
        self.title_ngs = self._app_context.ng.select("title")
        self.name_ngs = self._app_context.ng.select("name")
        self.id_ngs = self._app_context.ng.select("id")
        self.word_ngs = self._app_context.ng.select("word")

        self.on_property_changed("title_ngs")
        self.on_property_changed("name_ngs")
        self.on_property_changed("id_ngs")
        self.on_property_changed("word_ngs")
