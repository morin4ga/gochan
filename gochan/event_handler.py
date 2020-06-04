class EventHandler:
    def __init__(self):
        super().__init__()
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)

    def remove(self, handler):
        self._handlers.remove(handler)

    def __call__(self, args):
        for h in self._handlers:
            h(args)
