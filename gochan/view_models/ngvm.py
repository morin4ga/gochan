from typing import List

from gochan.models import AppContext
from gochan.models.ng import NGName, NGWord, NGId, NGTitle, NGItem  # noqa: F401
from gochan.event_handler import EventHandler


class NGVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._app_context.ng.on_collection_changed.add(self._ng_changed)
        self.on_property_changed = EventHandler()

    @property
    def names(self) -> List[NGName]:
        return self._app_context.ng.names

    @property
    def ids(self) -> List[NGId]:
        return self._app_context.ng.ids

    @property
    def words(self) -> List[NGWord]:
        return self._app_context.ng.words

    @property
    def titles(self) -> List[NGTitle]:
        return self._app_context.ng.titles

    def update_ng(self, id, values):
        self._app_context.ng.update_ng(id, values)

    def delete_ng(self, id):
        self._app_context.ng.delete_ng(id)

    def _ng_changed(self, property_name: str, type: str, item):
        self.on_property_changed(property_name)
