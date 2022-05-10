import constants as c
import pytest
from src.game.player import Player
from src.game.space import PropertySpace, PropertySet


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


@pytest.fixture
def player_comp():
    player = Player(
        name="Player 2",
        uid=1,
        token=3,
        properties=["Property 1", "Property 2"],
        cash=3000,
        position=10,
    )
    return player


@pytest.fixture
def prop_space_simple():
    property_set = PropertySet(set_id=0)
    property_space = PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        CONST_HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        CONST_HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_set.add_property(property_space)
    return property_space


def test_player_init(player_simple, player_comp):
    assert player_simple.name == "Player 1"
    assert player_simple.uid == 0
    assert player_simple.properties == []
    assert player_simple.cash.balance == 1500
    assert player_simple.position == 0

    assert player_comp.name == "Player 2"
    assert player_comp.uid == 1
    assert player_comp.token == 3
    assert player_comp.properties == ["Property 1", "Property 2"]
    assert player_comp.cash.balance == 3000
    assert player_comp.position == 10


def test_assign_token(player_simple, player_comp):
    player_simple.assign_token(5)
    player_comp.assign_token(10)
    assert player_simple.token == 5
    assert player_comp.token == 10


def test_move_player_from_zero(player_simple):
    assert player_simple.move(10) == 10
    assert player_simple.position == 10


def test_move_player_from_nonzero(player_comp):
    assert player_comp.move(10) == 20
    assert player_comp.position == 20


def test_add_property(player_simple, prop_space_simple):
    player_simple.add_property(prop_space_simple)
    assert len(player_simple.properties) == 1
    assert id(player_simple.properties[0]) == id(prop_space_simple)


def test_add_cash(player_comp):
    new_balance = player_comp.add_cash(1000)
    assert new_balance == 4000
    assert player_comp.cash.balance == 4000


def test_sub_cash(player_comp):
    new_balance = player_comp.sub_cash(500)
    assert new_balance == 2500
    assert player_comp.cash.balance == 2500


def test_offset_position(player_comp):
    pos = player_comp.move(25)
    pos = player_comp.offset_position(10)
    assert pos == 25
    assert player_comp.position == 25
