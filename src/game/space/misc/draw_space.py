from dataclasses import dataclass

import constants as c
from game.actions import Action

from ..space import Space


@dataclass(kw_only=True, slots=True)
class DrawSpace(Space):
    deck_type: c.DeckType  # DeckType.CONST_DECK_TYPE_CHANCE or DeckType.CONST_DECK_TYPE_CC

    def trigger(self) -> Action:
        if self.deck_type == c.DeckType.CONST_DECK_TYPE_CHANCE:
            return Action.DRAW_CHANCE_CARD
        elif self.deck_type == c.DeckType.CONST_DECK_TYPE_CC:
            return Action.DRAW_CC_CARD
        else:
            raise ValueError("Unknown deck type.")
