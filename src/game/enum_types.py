from enum import Enum, auto


class DeckType(Enum):
    CHANCE = auto()
    CC = auto()  # community chest


class TaxType(Enum):
    INCOME = auto()
    LUXURY = auto()
