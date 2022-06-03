from enum import Enum, auto


class Action(Enum):
    # No action to be triggered
    NOTHING = auto()

    # property card
    ASK_TO_BUY = auto()  # land on property card and ask if player wants to buy it
    START_AUCTION = auto()  # start the auction for property card
    PAY_RENT = auto()  # the player landed needs to pay rent

    # space
    CHARGE_INCOME_TAX = auto()  # the player landed on a income tax space, $200
    CHARGE_LUXURY_TAX = auto()  # the player landed on a luxury tax space, $100

    # charge fee for the bank
    CHARGE_GENERAL_REPAIR_FEE = auto()  # $25 for house, $100 for hotel
    CHARGE_POOR_TAX = auto()  # $15
    CHARGE_DOCTOR_FEE = auto()  # $50
    CHARGE_HOSPITAL_FEE = auto()  # $100
    CHARGE_SCHOOL_FEE = auto()  # $50
    CHARGE_STREET_REPAIR_FEE = auto()  # $40 for house, $115 for hotel

    # pay money to other players
    PAY_CHAIRMAN_FEE = auto()  # pay $50 to each player

    # movement
    ASK_TO_ROLL = auto()

    # send the player to a location
    SEND_TO_JAIL = auto()
    SEND_TO_GO = auto()
    SEND_TO_BOARDWALK = auto()
    SEND_TO_ILLINOIS_AVE = auto()
    SEND_TO_ST_CHARLES_PLACE = auto()
    SEND_TO_NEAREST_RAILROAD = auto()
    SEND_TO_NEAREST_UTILITY = auto()
    SEND_TO_READING_RAILROAD = auto()
    SEND_BACK_THREE_SPACES = auto()

    # collect something
    COLLECT_DIVIDEND = auto()  # $50
    COLLECT_JAIL_CARD = auto()
    COLLECT_LOAN = auto()  # $150
    COLLECT_BANK_ERROR = auto()  # $200
    COLLECT_STOCK_SALE = auto()  # $50
    COLLECT_GRAND_OPERA_NIGHT = auto()  # $50 from each player
    COLLECT_HOLIDAY_FUND = auto()  # $100
    COLLECT_TAX_REFUND = auto()  # $20
    COLLECT_BIRTHDAY = auto()  # $10 from each player
    COLLECT_INSURANCE = auto()  # $100
    COLLECT_CONSULTANCY_FEE = auto()  # $25
    COLLECT_CONTEST_PRIZE = auto()  # $10
    COLLECT_INHERITANCE = auto()  # $100

    # trigger checking/action?
    PASS_GO = auto()

    # event
    DRAW_CHANCE_CARD = auto()
    DRAW_CC_CARD = auto()
