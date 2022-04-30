import pytest

from player import Player
from constants import CONST_STARTING_CASH, CONST_GOAL_MONEY

@pytest.fixture
def player_simple():
    player = Player(name="Player 1", character=0)
    return player

@pytest.fixture
def player_comp():
    player = Player(
        name="Player 2",
        character=1,
        properties=["Property 1", "Property 2"],
        cash=3000,
        position=10
    )
    return player

def test_player_init(player_simple, player_comp):
    assert player_simple.name == 'Player 1'
    assert player_simple.character == 0
    assert player_simple.properties == []
    assert player_simple.cash.balance == 1500
    assert player_simple.position == 0

    assert player_comp.name == "Player 2"
    assert player_comp.character == 1
    assert player_comp.properties == ["Property 1", "Property 2"]
    assert player_comp.cash.balance == 3000
    assert player_comp.position == 10


def test_move_player(player_simple, player_comp):
    assert player_simple.move(10) == 10
    assert player_simple.position == 10

    assert player_comp.move(10) == 20
    assert player_comp.position == 20


def test_reset_player_position(player_simple, player_comp):
    player_simple.reset_position()
    assert player_simple.position == 0
    assert player_simple.cash.balance == CONST_STARTING_CASH + CONST_GOAL_MONEY

    player_comp.reset_position()
    assert player_comp.position == 0
    assert player_comp.cash.balance == 3000 + CONST_GOAL_MONEY


def test_reset_player_position_and_move(player_simple, player_comp):
    player_simple.reset_position()
    player_simple.move(10)
    assert player_simple.position == 10
    assert player_simple.cash.balance == CONST_STARTING_CASH + CONST_GOAL_MONEY

    player_comp.reset_position()
    player_comp.move(10)
    assert player_comp.position == 10
    assert player_comp.cash.balance == 3000 + CONST_GOAL_MONEY
