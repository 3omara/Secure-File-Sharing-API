from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Subject(ABC):
    def __init__(self):
        self.__observers: List[Observer] = []

    def register_observer(self, observer: Observer):
        self.__observers.append(observer)
        observer.update(self)

    def unregister_observer(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer(self)


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject):
        pass
