import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True, slots=True)
class User:
    # TODO remove optional and use init=False instead
    name: str
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    room_uid: Optional[str] = None  # assigned after joining a room
    player_uid: Optional[int] = None  # assigned after joining a game
