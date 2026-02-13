"""Холодильник основа"""

from .errors import DoorClosedError, UnknownZoneError
from .interfaces import DoorManager, StorageManager, Zone


class Fridge(DoorManager, StorageManager):
    """Двери+зоны"""

    def __init__(self, zones: list[Zone]) -> None:
        self._door_open = False
        self._zones: dict[str, Zone] = {}
        for zone in zones:
            if zone.name in self._zones:
                raise ValueError(f"Дубликат имени зоны: {zone.name}")
            self._zones[zone.name] = zone

    def open_door(self) -> bool:
        if self._door_open:
            return False
        self._door_open = True
        return True

    def close_door(self) -> bool:
        if not self._door_open:
            return False
        self._door_open = False
        return True

    def is_door_open(self) -> bool:
        return self._door_open

    def put_item(self, zone_name: str, item_name: str) -> None:
        self._require_open_door()
        zone = self._get_zone(zone_name)
        zone.add_item(item_name)

    def take_item(self, zone_name: str, item_name: str) -> None:
        self._require_open_door()
        zone = self._get_zone(zone_name)
        zone.remove_item(item_name)

    def list_items(self, zone_name: str) -> list[str]:
        zone = self._get_zone(zone_name)
        return zone.list_items()

    def list_all_items(self) -> dict[str, list[str]]:
        return {zone_name: zone.list_items() for zone_name, zone in self._zones.items()}

    def zone_names(self) -> list[str]:
        return list(self._zones.keys())

    def _require_open_door(self) -> None:
        if not self._door_open:
            raise DoorClosedError("Дверь закрыта. Сначала откройте холодильник.")

    def _get_zone(self, zone_name: str) -> Zone:
        zone = self._zones.get(zone_name)
        if zone is None:
            raise UnknownZoneError(
                f"Неизвестная зона '{zone_name}'. Доступные зоны: {', '.join(self.zone_names())}."
            )
        return zone
