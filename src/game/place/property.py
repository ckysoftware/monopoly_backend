from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from src.game.place.place import Place
from src.game.place.property_set import PropertySet


@dataclass
class Property(Place):
    price: int
    property_set: PropertySet
    mortgaged: bool = False
    owner_uid: int = None

    def assign_owner(self, player_uid) -> None:
        self.owner_uid = player_uid
        self.property_set.update_monopoly()

    @abstractmethod
    def compute_rent(self, **kwargs) -> int:
        pass

    # TODO may need to return money
    # NOTE probably can use default for utility_card, railroad_card, and only override property_card
    @abstractmethod
    def mortgage(self) -> None:  # NOTE probably need to return action/event
        pass

    # TODO may need to return money
    # NOTE probably can use default for utility_card, railroad_card, and only override property_card
    @abstractmethod
    def unmortgage(self) -> None:  # NOTE probably need to return action/event
        pass
