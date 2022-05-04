from __future__ import annotations

from dataclasses import dataclass, field

from src.game.actions import Action as a
from src.game.place.property import Property

from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.game.player import Player


@dataclass(kw_only=True)
class RailroadCard(Property):
    rent: list[int] = field(default_factory=list)

    def compute_rent(self) -> int:
        if self.mortgaged:
            return 0
        owned_stations = self.property_set.count_owned(self.owner_character)
        return self.rent[owned_stations - 1]

    def mortgage(self) -> None:
        if self.mortgaged:
            raise ValueError("Property is already mortgaged")
        elif self.owner_character is None:
            raise ValueError("Property has no owner")
        self.mortgaged = True

    # TODO unmortgage
    def unmortgage(self) -> None:
        pass

    def trigger(self, player: Player) -> int:
        if self.owner_character is None:
            return a.ASK_TO_BUY
        elif self.owner_character == player.character:
            return a.NOTHING
        elif self.owner_character != player.character:
            return a.CHARGE_RENT
        else:
            raise ValueError("Unknown action")
