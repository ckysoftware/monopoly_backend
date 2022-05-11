from dataclasses import dataclass, field

from game.player import Player
from game.space import Space

from game.actions import Action


@dataclass(kw_only=True, slots=True)
class GameMap:
    """
    This class represents the map of the game.
    """

    map_list: list[Space] = field(default_factory=list)
    size: int = None

    def __post_init__(self):
        self.size = len(self.map_list)

    def trigger(self, player: Player) -> Action:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
