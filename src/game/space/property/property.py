from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..space import Space

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from .property_set import PropertySet


@dataclass(kw_only=True, slots=True)
class Property(Space):
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
    # NOTE probably can use default for utility_space, railroad_space, and only override property_space
    @abstractmethod
    def mortgage(self) -> None:  # NOTE probably need to return action/event
        pass

    # TODO may need to return money
    # NOTE probably can use default for utility_space, railroad_space, and only override property_space
    @abstractmethod
    def unmortgage(self) -> None:  # NOTE probably need to return action/event
        pass
