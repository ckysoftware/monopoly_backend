import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


class EventType(enum.Enum):
    dice_roll = "dice_roll"
    move = "move"


@dataclass(slots=True)
class Event:
    """Base class for all events"""

    event_type: EventType
    message: dict[str, Any]
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class DiceRolled:
    """Event that is published when dice are rolled"""

    dice_1: int
    dice_2: int

    def __init__(self, dice_1: int, dice_2: int) -> None:
        self.dice_1 = dice_1
        self.dice_2 = dice_2
