"""Фабрики для создания стандартных объектов холодильника"""

from .fridge import Fridge
from .service import FridgeService
from .zones import DoorZone, MainZone, MedicineZone


def create_default_fridge() -> Fridge:
    return Fridge([MainZone(), DoorZone(), MedicineZone()])


def create_default_service() -> FridgeService:
    fridge = create_default_fridge()
    return FridgeService(door_manager=fridge, storage_manager=fridge)
