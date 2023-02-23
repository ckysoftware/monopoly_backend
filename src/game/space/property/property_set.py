from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from game import space

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from .property import Property


@dataclass(kw_only=True, slots=True)
class PropertySet:
    id: int
    properties: list[Property] = field(default_factory=list)
    monopoly: bool = False

    def add_property(self, property: Property) -> None:
        self.properties.append(property)

    def update_monopoly(self):
        if len(self.properties) == 0:
            self.monopoly = False
            return

        owner_uid = self.properties[0].owner_uid
        for property_ in self.properties[1:]:
            if property_.owner_uid is None or property_.owner_uid != owner_uid:
                self.monopoly = False
                return
        self.monopoly = True

    def count_owned(self, owner_uid: int):
        """
        Return the number of properties owned by this owner
        """
        count = 0
        for property_ in self.properties:
            if property_.owner_uid == owner_uid:
                count += 1
        return count

    def count_houses_and_hotels(self) -> tuple[int, int]:
        """
        Return the number of houses and hotels of all properties in the set
        """
        if not self.monopoly:
            return (0, 0)

        no_of_houses = no_of_hotels = 0

        for property_ in self.properties:
            assert isinstance(property_, space.PropertySpace)
            no_of_houses += property_.no_of_houses
            no_of_hotels += property_.no_of_hotels
        return no_of_houses, no_of_hotels

    def check_evenly_add_house_or_hotel(self, house_count: int) -> bool:
        """Check if a house or hotel can be remove based on the current house_count.
        Return true if it can, false otherwise"""
        return self._check_even_house_or_hotel(house_count, ops="add")

    def check_evenly_remove_house_or_hotel(self, house_count: int) -> bool:
        """Check if a house can be remove based on the current house_count.
        Return true if it can, false otherwise"""
        return self._check_even_house_or_hotel(house_count, ops="remove")

    def _check_even_house_or_hotel(self, house_count: int, ops: str) -> bool:
        """Check if a house can be add or remove based on the current house_count.
        ops is either 'add' or 'remove' to denote the operation to be checked.
        Return true if it can, false otherwise"""
        if not self.monopoly:
            return False

        assert ops in ("add", "remove")
        diff_offset = -1 if ops == "add" else 1

        for property_ in self.properties:
            assert isinstance(property_, space.PropertySpace)
            house_diff = (
                house_count
                - property_.no_of_houses
                - property_.no_of_hotels * (property_.HOUSE_LIMIT + 1)
            )
            if not (house_diff == 0 or house_diff == diff_offset):
                return False
        return True
