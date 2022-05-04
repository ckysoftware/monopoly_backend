from __future__ import annotations

from dataclasses import dataclass
from src.place import Place
from src.property_set import PropertySet


@dataclass
class Property(Place):
    price: int
    property_set: PropertySet
    mortgaged: bool = False
    owner_character: int = None

    def assign_owner(self, character) -> None:
        self.owner_character = character
        self.property_set.update_monopoly()

    def compute_rent(self) -> int:
        pass

    def mortgage(self) -> None:
        pass
