from dataclasses import dataclass

from game import enum_types, player
from game.actions import Action

from ..space import Space


@dataclass(kw_only=True, slots=True)
class DrawSpace(Space):
    deck_type: enum_types.DeckType

    def __post_init__(self):
        if not isinstance(self.deck_type, enum_types.DeckType):
            raise ValueError("Unknown deck type.")

    def trigger(self, player: player.Player) -> Action:
        if self.deck_type == enum_types.DeckType.CHANCE:
            return Action.DRAW_CHANCE_CARD
        elif self.deck_type == enum_types.DeckType.CC:
            return Action.DRAW_CC_CARD
