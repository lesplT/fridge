"""Интерфейсы(контракты)"""
from abc import ABC, abstractmethod


class Zone(ABC):
    """Интерфейс зоны хранения."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_item(self, item_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_item(self, item_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_items(self) -> list[str]:
        raise NotImplementedError


class DoorManager(ABC):
    """Только действия, связанные с дверцой."""

    @abstractmethod
    def open_door(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def close_door(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_door_open(self) -> bool:
        raise NotImplementedError


class StorageManager(ABC):
    """Только действия, связанные с предметами и зонами."""

    @abstractmethod
    def put_item(self, zone_name: str, item_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def take_item(self, zone_name: str, item_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_items(self, zone_name: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def list_all_items(self) -> dict[str, list[str]]:
        raise NotImplementedError

    @abstractmethod
    def zone_names(self) -> list[str]:
        raise NotImplementedError


class FridgeController(ABC):
    """Удобные для интерфейса операции, которые возвращают готовый к печати текст."""

    @abstractmethod
    def open(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def put(self, zone_name: str, item_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def take(self, zone_name: str, item_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def list_zone(self, zone_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def status(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def help_text(self) -> str:
        raise NotImplementedError
