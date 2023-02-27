import enum
from typing import TypedDict


class PropertyType(enum.Enum):
    PROPERTY = enum.auto()
    UTILITY = enum.auto()
    RAILROAD = enum.auto()


class BasePropertyData(TypedDict):
    id: int
    name: str
    price: int
    property_type: PropertyType
    property_set_id: int


class PropertyData(BasePropertyData):
    rent: list[int]
    price_of_house: int
    price_of_hotel: int


class RailroadData(BasePropertyData):
    rent: list[int]


class UtilityData(BasePropertyData):
    ...


CONST_PROPERTY_DATA: dict[int, PropertyData | RailroadData | UtilityData] = {
    0: {
        "id": 0,
        "name": "Mediterranean Avenue",
        "price": 60,
        "property_type": PropertyType.PROPERTY,
        "rent": [2, 10, 30, 90, 160, 250],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 0,
    },
    1: {
        "id": 1,
        "name": "Baltic Avenue",
        "price": 60,
        "property_type": PropertyType.PROPERTY,
        "rent": [4, 20, 60, 180, 320, 450],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 0,
    },
    2: {
        "id": 2,
        "name": "Oriental Avenue",
        "price": 100,
        "property_type": PropertyType.PROPERTY,
        "rent": [6, 30, 90, 270, 400, 550],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    3: {
        "id": 3,
        "name": "Vermont Avenue",
        "price": 100,
        "property_type": PropertyType.PROPERTY,
        "rent": [6, 30, 90, 270, 400, 550],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    4: {
        "id": 4,
        "name": "Connecticut Avenue",
        "price": 120,
        "property_type": PropertyType.PROPERTY,
        "rent": [8, 40, 100, 300, 450, 600],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    5: {
        "id": 5,
        "name": "St. Charles Place",
        "price": 140,
        "property_type": PropertyType.PROPERTY,
        "rent": [10, 50, 150, 450, 625, 750],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    6: {
        "id": 6,
        "name": "States Avenue",
        "price": 140,
        "property_type": PropertyType.PROPERTY,
        "rent": [10, 50, 150, 450, 625, 750],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    7: {
        "id": 7,
        "name": "Virginia Avenue",
        "price": 160,
        "property_type": PropertyType.PROPERTY,
        "rent": [12, 60, 180, 500, 700, 900],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    8: {
        "id": 8,
        "name": "St. James Place",
        "price": 180,
        "property_type": PropertyType.PROPERTY,
        "rent": [14, 70, 200, 550, 750, 950],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    9: {
        "id": 9,
        "name": "Tennessee Avenue",
        "price": 180,
        "property_type": PropertyType.PROPERTY,
        "rent": [14, 70, 200, 550, 750, 950],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    10: {
        "id": 10,
        "name": "New York Avenue",
        "price": 200,
        "property_type": PropertyType.PROPERTY,
        "rent": [16, 80, 220, 600, 800, 1000],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    11: {
        "id": 11,
        "name": "Kentucky Avenue",
        "price": 220,
        "property_type": PropertyType.PROPERTY,
        "rent": [18, 90, 250, 700, 875, 1050],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    12: {
        "id": 12,
        "name": "Indiana Avenue",
        "price": 220,
        "property_type": PropertyType.PROPERTY,
        "rent": [18, 90, 250, 700, 875, 1050],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    13: {
        "id": 13,
        "name": "Illinois Avenue",
        "price": 240,
        "property_type": PropertyType.PROPERTY,
        "rent": [20, 100, 300, 750, 925, 1100],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    14: {
        "id": 14,
        "name": "Atlantic Avenue",
        "price": 260,
        "property_type": PropertyType.PROPERTY,
        "rent": [22, 110, 330, 800, 975, 1150],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    15: {
        "id": 15,
        "name": "Ventnor Avenue",
        "price": 260,
        "property_type": PropertyType.PROPERTY,
        "rent": [22, 110, 330, 800, 975, 1150],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    16: {
        "id": 16,
        "name": "Marvin Gardens",
        "price": 280,
        "property_type": PropertyType.PROPERTY,
        "rent": [24, 120, 360, 850, 1025, 1200],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    17: {
        "id": 17,
        "name": "Pacific Avenue",
        "price": 300,
        "property_type": PropertyType.PROPERTY,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    18: {
        "id": 18,
        "name": "North Carolina Avenue",
        "price": 300,
        "property_type": PropertyType.PROPERTY,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    19: {
        "id": 19,
        "name": "Pennsylvania Avenue",
        "price": 320,
        "property_type": PropertyType.PROPERTY,
        "rent": [28, 150, 450, 1000, 1200, 1400],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    20: {
        "id": 20,
        "name": "Park Place",
        "price": 350,
        "property_type": PropertyType.PROPERTY,
        "rent": [35, 175, 500, 1100, 1300, 1500],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 7,
    },
    21: {
        "id": 21,
        "name": "Boardwalk",
        "price": 400,
        "property_type": PropertyType.PROPERTY,
        "rent": [50, 200, 600, 1400, 1700, 2000],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 7,
    },
    101: {
        "id": 101,
        "name": "Reading Railroad",
        "price": 200,
        "property_type": PropertyType.RAILROAD,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    102: {
        "id": 102,
        "name": "Pennsylvania Railroad",
        "price": 200,
        "property_type": PropertyType.RAILROAD,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    103: {
        "id": 103,
        "name": "B. & O. Railroad",
        "price": 200,
        "property_type": PropertyType.RAILROAD,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    104: {
        "id": 104,
        "name": "Short Line",
        "price": 200,
        "property_type": PropertyType.RAILROAD,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    111: {
        "id": 111,
        "name": "Electric Company",
        "price": 150,
        "property_set_id": 20,
        "property_type": PropertyType.UTILITY,
    },
    112: {
        "id": 112,
        "name": "Water Works",
        "price": 150,
        "property_set_id": 20,
        "property_type": PropertyType.UTILITY,
    },
}
