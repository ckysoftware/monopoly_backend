# flake8: noqa
from typing import TypedDict

from game.actions import Action


class CardData(TypedDict):
    id: int
    description: str
    action: Action
    ownable: bool


CONST_CHANCE_CARDS: list[CardData] = [
    {
        "id": 0,
        "description": "Advance to Boardwalk.",
        "action": Action.SEND_TO_BOARDWLAK,
        "ownable": False,
    },
    {
        "id": 1,
        "description": "Advance to Go (Collect $200).",
        "action": Action.SEND_TO_GO,
        "ownable": False,
    },
    {
        "id": 2,
        "description": "Advance to Illinois Ave. If you pass Go, collect $200.",
        "action": Action.SEND_TO_ILLINOIS_AVE,
        "ownable": False,
    },
    {
        "id": 3,
        "description": "Advance to St. Charles Place. If you pass Go, collect $200.",
        "action": Action.SEND_TO_ST_CHARLES_PLACE,
        "ownable": False,
    },
    {
        "id": 4,
        "description": "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled.",
        "action": Action.SEND_TO_NEAREST_RAILROAD,
        "ownable": False,
    },
    {
        "id": 5,
        "description": "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled.",
        "action": Action.SEND_TO_NEAREST_RAILROAD,
        "ownable": False,
    },
    {
        "id": 6,
        "description": "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.",
        "action": Action.SEND_TO_NEAREST_UTILITY,
        "ownable": False,
    },
    {
        "id": 7,
        "description": "Bank pays you dividend of $50.",
        "action": Action.COLLECT_DIVIDEND,
        "ownable": False,
    },
    {
        "id": 8,
        "description": "Get out of Jail Free. This card may be kept until needed, or traded/sold.",
        "action": Action.COLLECT_JAIL_CARD,
        "ownable": True,
    },
    {
        "id": 9,
        "description": "Go back 3 spaces.",
        "action": Action.SEND_BACK_THREE_SPACES,
        "ownable": False,
    },
    {
        "id": 10,
        "description": "Go to Jail. Go directly to Jail. Do not pass Go, do not collect $200.",
        "action": Action.SEND_TO_JAIL,
        "ownable": False,
    },
    {
        "id": 11,
        "description": "Make general repairs on all your property. For each house pay $25. For each hotel pay $100.",
        "action": Action.CHARGE_GENERAL_REPAIR_FEE,
        "ownable": False,
    },
    {
        "id": 12,
        "description": "Pay poor tax of $15.",
        "action": Action.CHARGE_POOR_TAX,
        "ownable": False,
    },
    {
        "id": 13,
        "description": "Take a trip to Reading Railroad. If you pass Go, collect $200.",
        "action": Action.SEND_TO_READING_RAILROAD,
        "ownable": False,
    },
    {
        "id": 14,
        "description": "You have been elected Chairman of the Board. Pay each player $50.",
        "action": Action.PAY_CHAIRMAN_FEE,
        "ownable": False,
    },
    {
        "id": 15,
        "description": "Your building and loan matures. Collect $150.",
        "action": Action.COLLECT_LOAN,
        "ownable": False,
    },
]


CONST_CC_CARDS: list[CardData] = [
    {
        "id": 100,
        "description": "Advance to Go (Collect $200).",
        "action": Action.SEND_TO_GO,
        "ownable": False,
    },
    {
        "id": 101,
        "description": "Bank error in your favor. Collect $200",
        "action": Action.COLLECT_BANK_ERROR,
        "ownable": False,
    },
    {
        "id": 102,
        "description": "Doctor's fee. Pay $50.",
        "action": Action.CHARGE_DOCTOR_FEE,
        "ownable": False,
    },
    {
        "id": 103,
        "description": "From sale of stock you get $50.",
        "action": Action.COLLECT_STOCK_SALE,
        "ownable": False,
    },
    {
        "id": 104,
        "description": "Get out of Jail Free. This card may be kept until needed, or traded/sold.",
        "action": Action.COLLECT_JAIL_CARD,
        "ownable": True,
    },
    {
        "id": 105,
        "description": "Go to Jail. Go directly to Jail. Do not pass Go, do not collect $200.",
        "action": Action.SEND_TO_JAIL,
        "ownable": False,
    },
    {
        "id": 106,
        "description": "Grand Opera Night. Collect $50 from every player for opening night seats.",
        "action": Action.COLLECT_GRAND_OPERA_NIGHT,
        "ownable": False,
    },
    {
        "id": 107,
        "description": "Holiday fund matures. Receive $100.",
        "action": Action.COLLECT_HOLIDAY_FUND,
        "ownable": False,
    },
    {
        "id": 108,
        "description": "Income tax refund. Collect $20.",
        "action": Action.COLLECT_TAX_REFUND,
        "ownable": False,
    },
    {
        "id": 109,
        "description": "It is your birthday. Collect $10 from every player.",
        "action": Action.COLLECT_BIRTHDAY,
        "ownable": False,
    },
    {
        "id": 110,
        "description": "Life insurance matures. Collect $100",
        "action": Action.COLLECT_INSURANCE,
        "ownable": False,
    },
    {
        "id": 111,
        "description": "Hospital Fees. Pay $100.",
        "action": Action.CHARGE_HOSPITAL_FEE,
        "ownable": False,
    },
    {
        "id": 112,
        "description": "School fees. Pay $50.",
        "action": Action.CHARGE_SCHOOL_FEE,
        "ownable": False,
    },
    {
        "id": 113,
        "description": "Receive $25 consultancy fee.",
        "action": Action.COLLECT_CONSULTANCY_FEE,
        "ownable": False,
    },
    {
        "id": 114,
        "description": "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
        "action": Action.CHARGE_STREET_REPAIR_FEE,
        "ownable": False,
    },
    {
        "id": 115,
        "description": "You have won second prize in a beauty contest. Collect $10.",
        "action": Action.COLLECT_CONTEST_PRIZE,
        "ownable": False,
    },
    {
        "id": 116,
        "description": "You inherit $100.",
        "action": Action.COLLECT_INHERITANCE,
        "ownable": False,
    },
]
