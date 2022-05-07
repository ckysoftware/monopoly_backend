import pytest
from game.game_map import GameMap
from game.place.property.property_card import PropertyCard
from game.place.property.property_set import PropertySet
from game.player import Player


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0)
    return player


@pytest.fixture
def prop_cards():
    property_set = PropertySet(set_id=0)
    property_card_1 = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=1,
    )
    property_card_2 = PropertyCard(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_card_1)
    property_set.add_property(property_card_2)
    return [property_card_1, property_card_2]


def test_game_map_init(prop_cards):
    game_map = GameMap(map_list=prop_cards)
    assert id(game_map.map_list[0]) == id(prop_cards[0])
    assert id(game_map.map_list[1]) == id(prop_cards[1])
    assert game_map.size == 2


def test_game_map_trigger(prop_cards, player_simple):
    game_map = GameMap(map_list=prop_cards)
    player_simple.character = 1
    player_simple.position = 0
    assert game_map.trigger(player_simple) == prop_cards[0].trigger(player_simple)
    player_simple.position = 1
    assert game_map.trigger(player_simple) == prop_cards[1].trigger(player_simple)
