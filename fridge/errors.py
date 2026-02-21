"""Доменные исключения для операций с холодильником"""


class FridgeError(Exception):
    """Базовая ошибка"""


class DoorClosedError(FridgeError):
    """Если операция требует открытой двери"""


class UnknownZoneError(FridgeError):
    """Если запрашиваемой зоны не существует"""


class ItemNotFoundError(FridgeError):
    """Если предмет в зоне не найден"""


class ZoneCapacityError(FridgeError):
    """Если зона полная"""
