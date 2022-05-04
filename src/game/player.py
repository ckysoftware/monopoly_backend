from dataclasses import dataclass, field

from src.game.cash import Cash
from src.game.place.property_card import PropertyCard

import src.constants as c


@dataclass
class Player:
    name: str
    character: int
    properties: list[PropertyCard] = field(default_factory=list)
    cash: Cash | int = c.CONST_STARTING_CASH
    position: int = 0

    def __post_init__(self):
        if isinstance(self.cash, int):
            self.cash = Cash(self.cash)

    def add_property(self, property: PropertyCard) -> None:
        self.properties.append(property)

    def move(self, steps) -> int:
        self.position += steps
        return self.position

    # TODO add parameter to reset without giving cash
    def reset_position(self) -> None:
        self.position = 0
        self.cash.add(c.CONST_GO_MONEY)

    # TODO roll dice and move player, also test for double roll
