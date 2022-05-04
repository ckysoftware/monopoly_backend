from dataclasses import dataclass, field

from src.card import Card
from src.player import Player


@dataclass
class GameMap():
    """
    This class represents the map of the game.
    """
    map_list: list[Card] = field(default_factory=list)

    def trigger(self, player: Player) -> int:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
