from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.game.actions import Action as a
from src.game.place.property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.game.player import Player


@dataclass(kw_only=True)
class UtilityCard(Property):
    def compute_rent(self, dice_count) -> int:
        if self.mortgaged:
            return 0
        elif self.property_set.monopoly:
            return dice_count * 10
        else:
            return dice_count * 4

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
            return a.ASK_TO_BUY
        elif self.owner_uid == player.uid:
            return a.NOTHING
        elif self.owner_uid != player.uid:
            return a.CHARGE_RENT
        else:
            raise ValueError("Unknown action")
