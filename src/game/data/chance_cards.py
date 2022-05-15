# flake8: noqa
from game.actions import Action

CONST_CHANCE_CARDS = [
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
