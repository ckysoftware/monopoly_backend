from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import src.constants as c
from src.game.actions import Action as a
from src.game.place.property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.game.player import Player


@dataclass(kw_only=True)
class PropertyCard(Property):
    rent: list[int]
    price_of_house: int
    price_of_hotel: int
    no_of_houses: int = 0
    no_of_hotels: int = 0

    def __post_init__(self):
        assert len(self.rent) == c.CONST_HOUSE_LIMIT + 2  # without + houses + hotel

    def assign_owner(self, character) -> None:
        self.owner_character = character
        self.property_set.update_monopoly()

    def compute_rent(self) -> int:
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

    # TODO check this later:
    """Before an improved property can be mortgaged,
    all the Houses and Hotels on all the properties of its color-group
    must be sold back to the Bank"""

    def mortgage(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_character is None:
            raise ValueError("Property has no owner")
        self.mortgaged = True

    # TODO remove mortgage
    def unmortgage(self) -> None:
        pass

    # TODO need to evenly add house, need to check
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

    def trigger(self, player: Player) -> int:
        if self.owner_character is None:
            return a.ASK_TO_BUY
        elif self.owner_character == player.character:
            return a.NOTHING
        elif self.owner_character != player.character:
            return a.CHARGE_RENT
        else:
            raise ValueError("Unknown action")
