from typing import TypedDict


class PropertyData(TypedDict):
    id: int
    name: str
    price: int
    rent: list[int]
    price_of_house: int
    price_of_hotel: int
    property_set_id: int


class RailroadData(TypedDict):
    id: int
    name: str
    price: int
    rent: list[int]
    property_set_id: int


class UtilityData(TypedDict):
    id: int
    name: str
    price: int
    property_set_id: int


CONST_PROPERTY_SPACES: list[PropertyData] = [
    {
        "id": 0,
        "name": "Mediterranean Avenue",
        "price": 60,
        "rent": [2, 10, 30, 90, 160, 250],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 0,
    },
    {
        "id": 1,
        "name": "Baltic Avenue",
        "price": 60,
        "rent": [4, 20, 60, 180, 320, 450],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 0,
    },
    {
        "id": 2,
        "name": "Oriental Avenue",
        "price": 100,
        "rent": [6, 30, 90, 270, 400, 550],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    {
        "id": 3,
        "name": "Vermont Avenue",
        "price": 100,
        "rent": [6, 30, 90, 270, 400, 550],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    {
        "id": 4,
        "name": "Connecticut Avenue",
        "price": 120,
        "rent": [8, 40, 100, 300, 450, 600],
        "price_of_house": 50,
        "price_of_hotel": 50,
        "property_set_id": 1,
    },
    {
        "id": 5,
        "name": "St. Charles Place",
        "price": 140,
        "rent": [10, 50, 150, 450, 625, 750],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    {
        "id": 6,
        "name": "States Avenue",
        "price": 140,
        "rent": [10, 50, 150, 450, 625, 750],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    {
        "id": 7,
        "name": "Virginia Avenue",
        "price": 160,
        "rent": [12, 60, 180, 500, 700, 900],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 2,
    },
    {
        "id": 8,
        "name": "St. James Place",
        "price": 180,
        "rent": [14, 70, 200, 550, 750, 950],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    {
        "id": 9,
        "name": "Tennessee Avenue",
        "price": 180,
        "rent": [14, 70, 200, 550, 750, 950],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    {
        "id": 10,
        "name": "New York Avenue",
        "price": 200,
        "rent": [16, 80, 220, 600, 800, 1000],
        "price_of_house": 100,
        "price_of_hotel": 100,
        "property_set_id": 3,
    },
    {
        "id": 11,
        "name": "Kentucky Avenue",
        "price": 220,
        "rent": [18, 90, 250, 700, 875, 1050],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    {
        "id": 12,
        "name": "Indiana Avenue",
        "price": 220,
        "rent": [18, 90, 250, 700, 875, 1050],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    {
        "id": 13,
        "name": "Illinois Avenue",
        "price": 240,
        "rent": [20, 100, 300, 750, 925, 1100],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 4,
    },
    {
        "id": 14,
        "name": "Atlantic Avenue",
        "price": 260,
        "rent": [22, 110, 330, 800, 975, 1150],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    {
        "id": 15,
        "name": "Ventnor Avenue",
        "price": 260,
        "rent": [22, 110, 330, 800, 975, 1150],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    {
        "id": 16,
        "name": "Marvin Gardens",
        "price": 280,
        "rent": [24, 120, 360, 850, 1025, 1200],
        "price_of_house": 150,
        "price_of_hotel": 150,
        "property_set_id": 5,
    },
    {
        "id": 17,
        "name": "Pacific Avenue",
        "price": 300,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    {
        "id": 18,
        "name": "North Carolina Avenue",
        "price": 300,
        "rent": [26, 130, 390, 900, 1100, 1275],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    {
        "id": 19,
        "name": "Pennsylvania Avenue",
        "price": 320,
        "rent": [28, 150, 450, 1000, 1200, 1400],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 6,
    },
    {
        "id": 20,
        "name": "Park Place",
        "price": 350,
        "rent": [35, 175, 500, 1100, 1300, 1500],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 7,
    },
    {
        "id": 21,
        "name": "Boardwalk",
        "price": 400,
        "rent": [50, 200, 600, 1400, 1700, 2000],
        "price_of_house": 200,
        "price_of_hotel": 200,
        "property_set_id": 7,
    },
]

CONST_RAILROAD_SPACES: list[RailroadData] = [
    {
        "id": 101,
        "name": "Reading Railroad",
        "price": 200,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    {
        "id": 102,
        "name": "Pennsylvania Railroad",
        "price": 200,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    {
        "id": 103,
        "name": "B. & O. Railroad",
        "price": 200,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
    {
        "id": 104,
        "name": "Short Line",
        "price": 200,
        "rent": [25, 50, 100, 200],
        "property_set_id": 10,
    },
]

CONST_UTILITY_SPACES: list[UtilityData] = [
    {
        "id": 111,
        "name": "Electric Company",
        "price": 150,
        "property_set_id": 20,
    },
    {
        "id": 112,
        "name": "Water Works",
        "price": 150,
        "property_set_id": 20,
    },
]
