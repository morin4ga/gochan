from typing import Optional
from gochan.models import AppContext
from gochan.event_handler import EventHandler


class NGVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = EventHandler()

        self.title_ngs = self._app_context.ng.filter("title")
        self.name_ngs = self._app_context.ng.filter("name")
        self.id_ngs = self._app_context.ng.filter("id")
        self.word_ngs = self._app_context.ng.filter("word")

    def add_item(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        self._app_context.ng.add_item(kind, value, use_reg, hide, board, key)

    def replace_item(self, target: id, kind: str, value: str, use_reg: bool, hide: bool,
                     board: Optional[str], key: Optional[str]):
        self._app_context.ng.replace_item(target, kind, value, use_reg, hide, board, key)

    def delete_item(self, target: id):
        self._app_context.ng.delete_item(target)

    def _ng_changed(self, sender, type: str, *arg):
        self.title_ngs = self._app_context.ng.filter("title")
        self.name_ngs = self._app_context.ng.filter("name")
        self.id_ngs = self._app_context.ng.filter("id")
        self.word_ngs = self._app_context.ng.filter("word")

        self.on_property_changed("title_ngs")
        self.on_property_changed("name_ngs")
        self.on_property_changed("id_ngs")
        self.on_property_changed("word_ngs")
