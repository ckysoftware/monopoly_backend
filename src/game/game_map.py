from dataclasses import dataclass, field
from typing import Optional, TypedDict

from game import space
from game.actions import Action
from game.player import Player


class SpaceDetails(TypedDict):
    name: str
    type: type
    price: Optional[int]
    property_set_id: Optional[int]
    rent: Optional[list[int]]
    price_of_house: Optional[int]
    price_of_hotel: Optional[int]
    mortgage_value: Optional[int]


@dataclass(kw_only=True, slots=True)
class GameMap:
    """
    This class represents the map of the game.
    """

    map_list: list[space.Space]
    size: int = field(init=False)

    def __post_init__(self):
        self.size = len(self.map_list)

    # TODO test this
    def get_space_name(self, position: int) -> str:
        return self.map_list[position].name

    # TODO test this
    def get_space_details(self, position: int) -> SpaceDetails:
        cur_space = self.map_list[position]
        details: SpaceDetails = {
            "name": cur_space.name,
            "type": type(cur_space),
            "price": getattr(cur_space, "price", None),
            "property_set_id": getattr(cur_space, "property_set_id", None),
            "rent": getattr(cur_space, "rent", None),
            "price_of_house": getattr(cur_space, "price_of_house", None),
            "price_of_hotel": getattr(cur_space, "price_of_hotel", None),
            "mortgage_value": getattr(cur_space, "mortgage_value", None),
        }

        return details

    def trigger(self, player: Player) -> Action:
        """
        This method triggers the card's action and action result.
        """
        return self.map_list[player.position].trigger(player)
