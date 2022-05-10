from dataclasses import dataclass

from src.game.actions import Action as A
from src.game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class NthSpace(Space):
    """
    Space that trigger no action
    """

    def trigger(self, player: Player) -> A:
        return A.NOTHING
