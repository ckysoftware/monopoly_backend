from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.actions import Action

from .property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.player import Player


@dataclass(kw_only=True, slots=True)
class UtilitySpace(Property):
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

    def trigger(self, player: Player) -> Action:
        if self.owner_uid is None:
            return Action.ASK_TO_BUY
        elif self.owner_uid == player.uid:
            return Action.NOTHING
        else:  # self.owner_uid != player.uid:
            return Action.PAY_RENT
