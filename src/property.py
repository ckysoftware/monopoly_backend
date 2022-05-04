from __future__ import annotations

from abc import abstractmethod
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

    @abstractmethod
    def compute_rent(self, **kwargs) -> int:
        pass

    # TODO may need to return money
    @abstractmethod
    def mortgage(self) -> None:  # NOTE probably need to return action/event
        pass

    # TODO may need to return money
    @abstractmethod
    def unmortgage(self) -> None:  # NOTE probably need to return action/event
        pass
