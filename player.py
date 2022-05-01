from dataclasses import dataclass, field

from cash import Cash
from property_card import PropertyCard

from constants import CONST_STARTING_CASH, CONST_GO_MONEY


@dataclass
class Player:
    name: str
    character: int
    properties: list = field(default_factory=list)
    cash: Cash | int = CONST_STARTING_CASH
    position: int = 0

    def __post_init__(self):
        if isinstance(self.cash, int):
            self.cash = Cash(self.cash)

    def add_property(self, property: PropertyCard) -> None:
        self.properties.append(property)

    def move(self, steps) -> int:
        self.position += steps
        return self.position

    def reset_position(self) -> None:
        self.position = 0
        self.cash.add(CONST_GO_MONEY)
