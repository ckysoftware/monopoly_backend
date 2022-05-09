from dataclasses import dataclass

from game.actions import Action as A
from game.player import Player
from game.space.space import Space


@dataclass(kw_only=True, slots=True)
class NthSpace(Space):
    """
    Space that trigger no action
    """

    def trigger(self, player: Player) -> A:
        return A.NOTHING
