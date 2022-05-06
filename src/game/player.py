from dataclasses import dataclass, field

import src.constants as c
from src.game.cash import Cash
from src.game.place.property_card import PropertyCard


@dataclass
class Player:
    name: str
    uid: int
    token: int = None
    properties: list[PropertyCard] = field(default_factory=list)
    cash: Cash | int = c.CONST_STARTING_CASH
    position: int = 0

    def __post_init__(self):
        if isinstance(self.cash, int):
            self.cash = Cash(self.cash)

    def add_property(self, property: PropertyCard) -> None:
        self.properties.append(property)

    def assign_token(self, token: int) -> None:
        self.token = token

    def move(self, steps) -> int:
        self.position += steps
        return self.position

    # TODO add parameter to reset without giving cash
    def reset_position(self) -> None:
        self.position = 0
        self.cash.add(c.CONST_GO_MONEY)

    # TODO roll dice and move player, also test for double roll
