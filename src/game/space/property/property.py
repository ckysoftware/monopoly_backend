from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..space import Space

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from .property_set import PropertySet


@dataclass(kw_only=True, slots=True)
class Property(Space):
    price: int
    property_set: PropertySet
    mortgaged: bool = False
    owner_uid: Optional[int] = None

    def assign_owner(self, player_uid: int) -> None:
        self.owner_uid = player_uid
        self.property_set.update_monopoly()

    @property
    def mortgage_value(self) -> int:
        return self.price // 2

    @property
    def property_set_id(self) -> int:
        return self.property_set.id

    def mortgage(self) -> int:  # NOTE probably need to return action/event
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_uid is None:
            raise ValueError("Property has no owner")

        self.mortgaged = True
        return self.mortgage_value

    def unmortgage(self) -> int:  # NOTE probably need to return action/event
        if not self.mortgaged:
            raise ValueError("Property is not mortgaged")

        self.mortgaged = False
        assert self.mortgage_value % 10 == 0, "Mortgage value is not a multiple of 10"
        return int(self.mortgage_value * 1.1)  # 10% interest

    @abstractmethod
    def compute_rent(self) -> int:
        ...
