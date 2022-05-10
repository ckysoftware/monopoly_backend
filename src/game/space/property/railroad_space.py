from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.game.actions import Action as A

from .property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.game.player import Player


@dataclass(kw_only=True, slots=True)
class RailroadSpace(Property):
    rent: list[int] = field(default_factory=list)

    def compute_rent(self) -> int:
        if self.mortgaged:
            return 0
        owned_stations = self.property_set.count_owned(self.owner_uid)
        return self.rent[owned_stations - 1]

    def mortgage(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_uid is None:
            raise ValueError("Property has no owner")
        self.mortgaged = True

    # TODO unmortgage
    def unmortgage(self) -> None:
        pass

    def trigger(self, player: Player) -> int:
        if self.owner_uid is None:
            return A.ASK_TO_BUY
        elif self.owner_uid == player.uid:
            return A.NOTHING
        else:  # self.owner_uid != player.uid:
            return A.CHARGE_RENT
