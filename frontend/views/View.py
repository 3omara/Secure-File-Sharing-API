from abc import ABC, abstractmethod

from App import App


class View(ABC):
    def __init__(self, parent):
        self.parent = parent

    def build(self, app: App):
        self.app = app
        self.setup_view()
        self.register_observers()

    @abstractmethod
    def setup_view(self):
        pass

    def register_observers(self):
        pass

    def unregister_observers(self):
        pass

    def __del__(self):
        self.unregister_observers()
