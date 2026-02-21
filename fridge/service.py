"""CLI и тгбот"""

from .errors import FridgeError
from .interfaces import DoorManager, FridgeController, StorageManager


class FridgeService(FridgeController):
    """Преобразует действия домена в удобные текстовые ответы."""

    def __init__(self, door_manager: DoorManager, storage_manager: StorageManager) -> None:
        self._door_manager = door_manager
        self._storage_manager = storage_manager
        self._zone_aliases = {
            "main": "main",
            "door": "door",
            "medicine": "medicine",
            "med": "medicine",
            "meds": "medicine",
            "drugs": "medicine",
        }

    def open(self) -> str:
        if self._door_manager.open_door():
            return "Дверь открыта."
        return "Дверь уже открыта."

    def close(self) -> str:
        if self._door_manager.close_door():
            return "Дверь закрыта."
        return "Дверь уже закрыта."

    def put(self, zone_name: str, item_name: str) -> str:
        zone_name = self._normalize_zone(zone_name)
        item_name = item_name.strip()
        if not item_name:
            return "Название предмета не может быть пустым."

        try:
            self._storage_manager.put_item(zone_name, item_name)
            return f"Добавлен(о/а) '{item_name}' в '{zone_name}'."
        except (FridgeError, ValueError) as error:
            return str(error)

    def take(self, zone_name: str, item_name: str) -> str:
        zone_name = self._normalize_zone(zone_name)
        item_name = item_name.strip()
        if not item_name:
            return "Название предмета не может быть пустым."

        try:
            self._storage_manager.take_item(zone_name, item_name)
            return f"Убран(о/а) '{item_name}' из '{zone_name}'."
        except (FridgeError, ValueError) as error:
            return str(error)

    def list_zone(self, zone_name: str) -> str:
        zone_name = self._normalize_zone(zone_name)
        try:
            items = self._storage_manager.list_items(zone_name)
        except FridgeError as error:
            return str(error)
        return self._format_zone(zone_name, items)

    def list_all(self) -> str:
        data = self._storage_manager.list_all_items()
        lines = [self._format_zone(zone_name, items) for zone_name, items in data.items()]
        return "\n".join(lines)

    def status(self) -> str:
        door_state = "открыта" if self._door_manager.is_door_open() else "закрыта"
        return f"Дверь: {door_state}\n{self.list_all()}"

    def help_text(self) -> str:
        return (
            "Команды:\n"
            "  open\n"
            "  close\n"
            "  put <зона> <объект>\n"
            "  take <зона> <объект>\n"
            "  list [зона]\n"
            "  status\n"
            "  help\n"
            "  exit\n\n"
            "Зоны: main, door, medicine (алиасы: med, meds, drugs)."
        )

    def _normalize_zone(self, zone_name: str) -> str:
        normalized = zone_name.strip().lower()
        return self._zone_aliases.get(normalized, normalized)

    @staticmethod
    def _format_zone(zone_name: str, items: list[str]) -> str:
        if not items:
            return f"{zone_name}: пусто"
        return f"{zone_name}: {', '.join(items)}"
