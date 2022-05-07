from dataclasses import dataclass, field

import constants as c

from game.cash import Cash
from game.place.property.property_card import PropertyCard


@dataclass(kw_only=True, slots=True)
class Player:
    name: str
    uid: int
    token: int = None
    properties: list[PropertyCard] = field(default_factory=list)
    cash: Cash | int = c.CONST_STARTING_CASH
    position: int = 0

    def __post_init__(self):
        if isinstance(self.cash, int):
            self.cash = Cash(balance=self.cash)

    def add_property(self, property: PropertyCard) -> None:
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
        self.cash.add(amount)
        return self.cash.balance

    def sub_cash(self, amount: int) -> int:
        self.cash.sub(amount)
        return self.cash.balance

    # TODO roll dice and move player, also test for double roll
