from gochan.event_handler import PropertyChangedEventHandler, PropertyChangedEventArgs
from gochan.models import AppContext
from gochan.models.favorites import Favorites


class FavoritesVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        s


