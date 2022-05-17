from dataclasses import dataclass

from game import enum_types
from game.actions import Action
from game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class TaxSpace(Space):
    tax_type: enum_types.TaxType

    def trigger(self, player: Player) -> Action:
        if self.tax_type == enum_types.TaxType.INCOME:
            return Action.CHARGE_INCOME_TAX
        elif self.tax_type == enum_types.TaxType.LUXURY:
            return Action.CHARGE_LUXURY_TAX
        else:
            raise ValueError("Unknown tax type.")
