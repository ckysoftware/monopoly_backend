from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.actions import Action

from .property import Property

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.player import Player


@dataclass(kw_only=True, slots=True)
class UtilitySpace(Property):
    def compute_rent(self, dice_count: int = 0) -> int:
        if dice_count <= 0:
            raise ValueError("Dice count must be positive")
        if self.mortgaged:
            return 0
        elif self.property_set.monopoly:
            return dice_count * 10
        else:
            return dice_count * 4

    def trigger(self, player: Player) -> Action:
        if self.owner_uid is None:
            return Action.ASK_TO_BUY
        elif self.owner_uid == player.uid:
            return Action.NOTHING
        else:  # self.owner_uid != player.uid:
            return Action.PAY_RENT
