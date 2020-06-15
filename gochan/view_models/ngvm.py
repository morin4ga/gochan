from gochan.models import AppContext


class NGViewModel:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context

    @property
    def config(self):
        return self._app_context.ng.get_all_config()
