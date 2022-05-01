from dataclasses import dataclass

from card import Card

import constants as c
from property_set import PropertySet


@dataclass(kw_only=True)
class PropertyCard(Card):
    price: int
    rent: list[int]
    price_of_house: int
    price_of_hotel: int
    property_set: PropertySet
    no_of_houses: int = 0
    no_of_hotels: int = 0
    mortgaged: bool = False
    owner_character: int = None

    def __post_init__(self):
        assert len(self.rent) == c.CONST_HOUSE_LIMIT + 2  # without + houses + hotel

    def assign_owner(self, character) -> None:
        self.owner_character = character
        self.property_set.update_monopoly()

    def get_rent(self) -> int:
        if self.mortgaged:
            return 0
        elif self.no_of_hotels > 0:
            return self.rent[-1]
        elif self.no_of_houses > 0:
            return self.rent[self.no_of_houses]
        elif self.property_set.monopoly:
            return self.rent[0] * 2
        else:
            return self.rent[0]

    def mortgage(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_character is None:
            raise ValueError("Property has no owner")
        self.mortgaged = True

    def add_house(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is mortgaged")
        if self.no_of_houses == c.CONST_HOUSE_LIMIT:
            raise ValueError("House limit reached")
        if not self.property_set.monopoly:
            raise ValueError("Property is not in monopoly")
        self.no_of_houses += 1

    def add_hotel(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is mortgaged")
        if self.no_of_houses != c.CONST_HOUSE_LIMIT:
            raise ValueError("Not enough houses")
        if self.no_of_hotels == c.CONST_HOTEL_LIMIT:
            raise ValueError("Hotel limit reached")
        self.no_of_houses = 0
        self.no_of_hotels = 1

    def remove_house(self) -> None:
        if self.no_of_houses == 0:
            raise ValueError("No houses to remove")
        self.no_of_houses -= 1

    def remove_hotel(self) -> None:
        if self.no_of_hotels == 0:
            raise ValueError("No hotels to remove")
        self.no_of_hotels = 0
        self.no_of_houses = c.CONST_HOUSE_LIMIT
