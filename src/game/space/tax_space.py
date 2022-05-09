from dataclasses import dataclass

from game.actions import Action as A
from game.player import Player
from game.space.space import Space


@dataclass(kw_only=True, slots=True)
class TaxSpace(Space):
    TAX_ACTION: A

    def __post_init__(self):
        if not (
            self.TAX_ACTION == A.CHARGE_INCOME_TAX
            or self.TAX_ACTION == A.CHARGE_LUXARY_TAX
        ):
            raise ValueError(
                "Tax space must have a TAX_ACTION of either CHARGE_INCOME_TAX or CHARGE_LUXARY_TAX"
            )

    def trigger(self, _: Player) -> A:
        return self.TAX_ACTION
