from dataclasses import dataclass, field

from game.place.place import Place
from game.player import Player


@dataclass(kw_only=True)
class GameMap:
    """
    This class represents the map of the game.
    """

    map_list: list[Place] = field(default_factory=list)
    size: int = None

    def __post_init__(self):
        self.size = len(self.map_list)

    def trigger(self, player: Player) -> int:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
