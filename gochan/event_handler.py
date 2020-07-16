from abc import ABC, abstractmethod
from enum import Enum


class EventHandler(ABC):
    def __init__(self):
        super().__init__()
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)

    def remove(self, handler):
        self._handlers.remove(handler)

    @abstractmethod
    def invoke(self, args):
        pass


class PropertyChangedEventArgs:
    def __init__(self, sender, property_name: str):
        super().__init__()
        self.sender = sender
        self.property_name = property_name


class PropertyChangedEventHandler(EventHandler):
    def invoke(self, args: PropertyChangedEventArgs):
        for h in self._handlers:
            h(args)


class CollectionChangedEventKind(Enum):
    ADD = 0
    EXTEND = 1
    CHANGE = 2
    DELETE = 3


class CollectionChangedEventArgs:
    def __init__(self, sender, property_name: str, kind: CollectionChangedEventKind, item):
        super().__init__()
        self.sender = sender
        self.property_name = property_name
        self.kind = kind
        self.item = item


class CollectionChangedEventHandler(EventHandler):
    def invoke(self, args: CollectionChangedEventArgs):
        for h in self._handlers:
            h(args)
