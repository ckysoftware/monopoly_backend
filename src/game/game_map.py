from dataclasses import dataclass, field

from src.game.player import Player
from src.game.space import Space


@dataclass(kw_only=True, slots=True)
class GameMap:
    """
    This class represents the map of the src.game.
    """

    map_list: list[Space] = field(default_factory=list)
    size: int = None

    def __post_init__(self):
        self.size = len(self.map_list)

    def trigger(self, player: Player) -> int:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
