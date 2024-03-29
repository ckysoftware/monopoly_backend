from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.actions import Action

from .property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.player import Player


@dataclass(kw_only=True, slots=True)
class PropertySpace(Property):
    rent: list[int]
    price_of_house: int
    price_of_hotel: int
    HOUSE_LIMIT: int
    HOTEL_LIMIT: int
    no_of_houses: int = 0
    no_of_hotels: int = 0

    def __post_init__(self):
        assert len(self.rent) == self.HOUSE_LIMIT + 2  # without + houses + hotel

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

    # TODO test this
    def allow_mortgage(self) -> bool:
        set_no_of_houses, set_no_of_hotels = self.property_set.count_houses_and_hotels()
        if (
            self.mortgaged
            or self.owner_uid is None
            or self.no_of_houses != 0
            or self.no_of_hotels != 0
            or set_no_of_houses != 0
            or set_no_of_hotels != 0
        ):
            return False
        return True

    def mortgage(self) -> int:
        """Return the amount of cash to receive"""
        no_of_houses, no_of_hotels = self.property_set.count_houses_and_hotels()
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_uid is None:
            raise ValueError("Property has no owner")
        elif no_of_houses != 0 or no_of_hotels != 0:
            raise ValueError("Property set has houses or hotels")
        self.mortgaged = True
        return self.mortgage_value

    # TODO add test for all allow checks
    def allow_add_house(self) -> bool:
        if (
            self.mortgaged
            or self.no_of_houses == self.HOUSE_LIMIT
            or not self.property_set.monopoly
            or not self.property_set.check_evenly_add_house_or_hotel(self.no_of_houses)
        ):
            return False
        return True

    def add_house(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is mortgaged")
        if self.no_of_houses == self.HOUSE_LIMIT:
            raise ValueError("House limit reached")
        if not self.property_set.monopoly:
            raise ValueError("Property is not in monopoly")
        if not self.property_set.check_evenly_add_house_or_hotel(self.no_of_houses):
            raise ValueError("Houses are not evenly distributed in the property set")
        self.no_of_houses += 1

    def allow_add_hotel(self) -> bool:
        if (
            self.mortgaged
            or self.no_of_hotels == self.HOTEL_LIMIT
            or self.no_of_houses != self.HOUSE_LIMIT
            or not self.property_set.monopoly
            or not self.property_set.check_evenly_add_house_or_hotel(self.no_of_houses)
        ):
            return False
        return True

    def add_hotel(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is mortgaged")
        if self.no_of_hotels == self.HOTEL_LIMIT:
            raise ValueError("Hotel limit reached")
        if self.no_of_houses != self.HOUSE_LIMIT:
            raise ValueError("Not enough houses")
        if not self.property_set.monopoly:
            raise ValueError("Property is not in monopoly")
        if not self.property_set.check_evenly_add_house_or_hotel(self.no_of_houses):
            raise ValueError("Houses are not evenly distributed in the property set")
        self.no_of_houses = 0
        self.no_of_hotels = 1

    def allow_remove_house(self) -> bool:
        if (
            self.no_of_houses == 0
            or not self.property_set.check_evenly_remove_house_or_hotel(
                self.no_of_houses
            )
        ):
            return False
        return True

    def remove_house(self) -> None:
        if self.no_of_houses == 0:
            raise ValueError("No houses to remove")
        if not self.property_set.check_evenly_remove_house_or_hotel(self.no_of_houses):
            raise ValueError("Houses are not evenly distributed in the property set")
        self.no_of_houses -= 1

    def allow_remove_hotel(self) -> bool:
        if self.no_of_hotels == 0:
            return False
        return True

    def remove_hotel(self) -> None:
        # No need to check evenly remove hotel because it must be true
        if self.no_of_hotels == 0:
            raise ValueError("No hotels to remove")
        self.no_of_hotels = 0
        self.no_of_houses = self.HOUSE_LIMIT

    def trigger(self, player: Player) -> Action:
        if self.owner_uid is None:
            return Action.ASK_TO_BUY
        elif self.owner_uid == player.uid:
            return Action.NOTHING
        else:  # self.owner_uid != player.uid:
            return Action.PAY_RENT
