from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game import space


@dataclass(kw_only=True, slots=True)
class Player:
    name: str
    uid: int  # TODO change to id, unless use uuid
    cash: int
    token: int | None = None
    properties: list[space.Property] = field(default_factory=list)
    position: int = 0

    def __eq__(self, other: Player):
        return self.uid == other.uid

    def add_property(self, property_: space.Property) -> None:
        self.properties.append(property_)

    def assign_token(self, token: int) -> None:
        self.token = token

    def move(self, position: Optional[int] = None, steps: Optional[int] = None) -> int:
        """Move player either by steps or map position"""
        if position is not None:
            self.position = position
        elif steps is not None:
            self.position += steps
        else:
            raise ValueError("Either steps or position must be provided")
        return self.position

    def offset_position(self, offset: int) -> int:
        # offset position after passing Go
        self.position -= offset
        return self.position

    def add_cash(self, amount: int) -> int:
        self.cash += amount
        return self.cash

    def sub_cash(self, amount: int) -> int:
        self.cash -= amount
        return self.cash
