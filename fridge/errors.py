"""Domain-level errors for fridge operations."""


class FridgeError(Exception):
    """Base error for all fridge failures."""


class DoorClosedError(FridgeError):
    """Raised when operation requires an open door."""


class UnknownZoneError(FridgeError):
    """Raised when the requested zone does not exist."""


class ItemNotFoundError(FridgeError):
    """Raised when an item is missing in a zone."""


class ZoneCapacityError(FridgeError):
    """Raised when a zone is full."""
