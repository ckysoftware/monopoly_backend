from enum import Enum, auto


class Action(Enum):
    # No action to be triggered
    NOTHING = auto()

    # property card
    ASK_TO_BUY = auto()  # land on property card and ask if player wants to buy it
    START_AUCTION = auto()  # start the auction for property card
    CHARGE_RENT = auto()  # the player landed needs to pay rent

    # space
    CHARGE_INCOME_TAX = auto()  # the player landed on a income tax space
    CHARGE_LUXARY_TAX = auto()  # the player landed on a luxary tax space

    # movement
    ASK_TO_ROLL = auto()

    # event
    SEND_TO_JAIL = auto()

    PASS_GO = auto()
