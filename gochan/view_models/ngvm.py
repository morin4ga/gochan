from typing import Optional
from gochan.models import AppContext
from gochan.event_handler import EventHandler


class NGVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._app_context.ng.on_property_changed.add(self._context_changed)
        self.on_property_changed = EventHandler()

        self.title_ngs = list(filter(lambda x: x.kind == "title", self._app_context.ng.list))
        self.name_ngs = list(filter(lambda x: x.kind == "name", self._app_context.ng.list))
        self.id_ngs = list(filter(lambda x: x.kind == "id", self._app_context.ng.list))
        self.word_ngs = list(filter(lambda x: x.kind == "word", self._app_context.ng.list))

    @property
    def ng(self):
        return self._app_context.ng

    def add_item(self, kind: str, value: str, use_reg: bool, hide: bool, board: Optional[str], key: Optional[str]):
        self._app_context.ng.add_item(kind, value, use_reg, hide, board, key)

    def replace_item(self, target: id, kind: str, value: str, use_reg: bool, hide: bool,
                     board: Optional[str], key: Optional[str]):
        self._app_context.ng.replace_item(target, kind, value, use_reg, hide, board, key)

    def delete_item(self, target: id):
        self._app_context.ng.delete_item(target)

    def _context_changed(self, property_name: str):
        self.title_ngs = list(filter(lambda x: x.kind == "title", self._app_context.ng.list))
        self.name_ngs = list(filter(lambda x: x.kind == "name", self._app_context.ng.list))
        self.id_ngs = list(filter(lambda x: x.kind == "id", self._app_context.ng.list))
        self.word_ngs = list(filter(lambda x: x.kind == "word", self._app_context.ng.list))

        self.on_property_changed("ng")
        self.on_property_changed("title_ngs")
        self.on_property_changed("name_ngs")
        self.on_property_changed("id_ngs")
        self.on_property_changed("word_ngs")
