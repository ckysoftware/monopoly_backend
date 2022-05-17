import constants as c
import pytest
from game import player, space
from game.game_map import GameMap


@pytest.fixture
def prop_spaces():
    property_set = space.PropertySet(id=0)
    property_space_1 = space.PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=1,
    )
    property_space_2 = space.PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    return [property_space_1, property_space_2]


def test_game_map_init(prop_spaces: list[space.Space]):
    game_map = GameMap(map_list=prop_spaces)
    assert id(game_map.map_list[0]) == id(prop_spaces[0])
    assert id(game_map.map_list[1]) == id(prop_spaces[1])
    assert game_map.size == 2


def test_game_map_trigger(prop_spaces: list[space.Space], player_simple: player.Player):
    game_map = GameMap(map_list=prop_spaces)
    player_simple.uid = 1
    player_simple.position = 0
    assert game_map.trigger(player_simple) == prop_spaces[0].trigger(player_simple)
    player_simple.position = 1
    assert game_map.trigger(player_simple) == prop_spaces[1].trigger(player_simple)
