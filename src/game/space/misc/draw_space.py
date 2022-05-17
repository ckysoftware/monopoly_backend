from dataclasses import dataclass

from game import enum_types
from game.actions import Action
from game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class DrawSpace(Space):
    deck_type: enum_types.DeckType

    def trigger(self, player: Player) -> Action:
        if self.deck_type == enum_types.DeckType.CHANCE:
            return Action.DRAW_CHANCE_CARD
        elif self.deck_type == enum_types.DeckType.CC:
            return Action.DRAW_CC_CARD
        else:
            raise ValueError("Unknown deck type.")
