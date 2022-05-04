from enum import Enum, auto


class Action(Enum):
    # No action to be triggered
    NOTHING = auto()

    # property card
    ASK_TO_BUY = auto()  # land on property card and ask if player wants to buy it
    START_AUCTION = auto()  # start the auction for property card
    CHARGE_RENT = auto()  # the player landed needs to pay rent
