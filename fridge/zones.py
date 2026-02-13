"""Зоны"""

from .errors import ItemNotFoundError, ZoneCapacityError
from .interfaces import Zone


class BaseZone(Zone):
    """Общая реализация"""

    def __init__(self, name: str, capacity: int) -> None:
        self._name = name
        self._capacity = capacity
        self._items: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    def add_item(self, item_name: str) -> None:
        item_name = item_name.strip()
        if not item_name:
            raise ValueError("item_name не может быть пустым.")
        if len(self._items) >= self._capacity:
            raise ZoneCapacityError(f"Зона '{self._name}' полна.")
        self._items.append(item_name)

    def remove_item(self, item_name: str) -> None:
        item_name = item_name.strip()
        try:
            self._items.remove(item_name)
        except ValueError as error:
            raise ItemNotFoundError(
                f"'{item_name}' не найден(о/а) в зоне '{self._name}'."
            ) from error

    def list_items(self) -> list[str]:
        return list(self._items)


class MainZone(BaseZone):
    def __init__(self) -> None:
        super().__init__(name="main", capacity=20)


class DoorZone(BaseZone):
    def __init__(self) -> None:
        super().__init__(name="door", capacity=12)


class MedicineZone(BaseZone):
    def __init__(self) -> None:
        super().__init__(name="medicine", capacity=5)
