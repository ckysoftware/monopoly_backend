from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.space import PropertySpace


@dataclass(kw_only=True, slots=True)
class Player:
    name: str
    uid: int  # TODO change to id, unless use uuid
    cash: int
    token: int | None = None
    properties: list[PropertySpace] = field(default_factory=list)
    position: int = 0

    def add_property(self, property: PropertySpace) -> None:
        self.properties.append(property)

    def assign_token(self, token: int) -> None:
        self.token = token

    def move(self, steps: int) -> int:
        self.position += steps
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

    # TODO test this
    def send_to_pos(self, position: int) -> None:
        self.position = position

    # TODO roll dice and move player, also test for double roll
