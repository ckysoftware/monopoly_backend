from dataclasses import dataclass

from src.game.actions import Action
from src.game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class NthSpace(Space):
    """
    Space that trigger no action
    """

    def trigger(self, player: Player) -> Action:
        return Action.NOTHING
