from dataclasses import dataclass

from game.card.deck import Deck
from game.space.space import Space


@dataclass(kw_only=True, slots=True)
class DrawSpace(Space):
    deck: Deck  # deck containing cards to be drawn
