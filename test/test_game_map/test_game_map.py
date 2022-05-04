import pytest
from src.game.player import Player
from src.game.place.property_card import PropertyCard
from src.game.place.property_set import PropertySet
from src.game.game_map import GameMap


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", character=0)
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
        owner_character=1,
    )
    property_card_2 = PropertyCard(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_character=10,
    )
    property_set.add_property(property_card_1)
    property_set.add_property(property_card_2)
    return [property_card_1, property_card_2]


def test_game_map_init(prop_cards):
    game_map = GameMap(prop_cards)
    assert id(game_map.map_list[0]) == id(prop_cards[0])
    assert id(game_map.map_list[1]) == id(prop_cards[1])


def test_game_map_trigger(prop_cards, player_simple):
    game_map = GameMap(prop_cards)
    player_simple.character = 1
    player_simple.position = 0
    assert game_map.trigger(player_simple) == prop_cards[0].trigger(player_simple)
    player_simple.position = 1
    assert game_map.trigger(player_simple) == prop_cards[1].trigger(player_simple)
