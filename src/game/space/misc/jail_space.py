from dataclasses import dataclass

from game.actions import Action
from game.player import Player

from ..space import Space


@dataclass(kw_only=True, slots=True)
class JailSpace(Space):
    """
    Space that trigger SEND_TO_JAIL action
    """

    def trigger(self, player: Player) -> Action:
        return Action.SEND_TO_JAIL
