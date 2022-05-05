from dataclasses import dataclass, field

from src.game.place.place import Place
from src.game.player import Player


@dataclass
class GameMap:
    """
    This class represents the map of the game.
    """

    map_list: list[Place] = field(default_factory=list)

    def trigger(self, player: Player) -> int:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
