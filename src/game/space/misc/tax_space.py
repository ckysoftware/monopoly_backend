from dataclasses import dataclass

from src.game.actions import Action
from src.game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class TaxSpace(Space):
    TAX_ACTION: Action

    def __post_init__(self):
        if not (
            self.TAX_ACTION == Action.CHARGE_INCOME_TAX
            or self.TAX_ACTION == Action.CHARGE_LUXARY_TAX
        ):
            raise ValueError(
                "Tax space must have a TAX_ACTION of either CHARGE_INCOME_TAX or CHARGE_LUXARY_TAX"
            )

    def trigger(self, _: Player) -> Action:
        return self.TAX_ACTION
