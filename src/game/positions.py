from enum import IntEnum


class Position(IntEnum):
    """Contains the position of the Space"""

    GO = 0
    READING_RAILROAD = 5
    JAIL = 10
    ST_CHARLES_PLACE = 11
    ILLINOIS_AVE = 24
    BOARDWLAK = 39

    UTILITIES = [12, 28]
    RAILROADS = [5, 15, 25, 35]
