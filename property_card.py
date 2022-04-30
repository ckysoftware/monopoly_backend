from dataclasses import dataclass

from card import Card

from constants import CONST_HOUSE_LIMIT, CONST_HOTEL_LIMIT

@dataclass(kw_only=True)
class PropertyCard(Card):
    price: int
    rent: dict(int, int)
    price_of_house: int
    price_of_hotel: int
    property_set: int  # id for the property set
    no_of_houses: int = 0
    no_of_hotels: int = 0
    mortgaged: bool = False
    owner_character: int = None

    def add_house(self):
        if self.no_of_houses == CONST_HOUSE_LIMIT:
            raise ValueError("House limit reached")
        self.no_of_houses += 1
    
    def add_hotel(self):
        if self.no_of_hotels == CONST_HOTEL_LIMIT:
            raise ValueError("Hotel limit reached")
        self.no_of_houses = 0
        self.no_of_hotels = 1

    def rent(self, monopoly: bool):
        return 100  # TODO return rent based on state, also handle x2 rent

    # TODO maybe only need sell or mortgage?
    def remove_house(self):
        if self.no_of_houses == 0:
            raise ValueError("No houses to remove")
        self.no_of_houses -= 1
    
    # TODO maybe only need sell or mortgage?
    def remove_hotel(self):
        if self.no_of_hotels == 0:
            raise ValueError("No hotels to remove")
        self.no_of_hotels = 0
        self.no_of_houses = 0

