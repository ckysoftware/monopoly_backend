from enum import Enum, auto

# Game Settings
CONST_STARTING_CASH = 1500
CONST_GO_MONEY = 200

CONST_HOUSE_MAX = 32
CONST_HOTEL_MAX = 12
CONST_MAX_DOUBLE_ROLL = 3

# Property
CONST_HOUSE_LIMIT = 4
CONST_HOTEL_LIMIT = 1


# Card deck type
class DeckType(Enum):
    CONST_DECK_TYPE_CHANCE = auto()
    CONST_DECK_TYPE_CC = auto()
