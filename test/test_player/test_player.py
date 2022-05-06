import pytest
import src.constants as c
from src.game.player import Player


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0)
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


def test_reset_player_position_from_zero(player_simple):
    player_simple.reset_position()
    assert player_simple.position == 0
    assert player_simple.cash.balance == c.CONST_STARTING_CASH + c.CONST_GO_MONEY


def test_reset_player_position_from_nonzero(player_comp):
    player_comp.reset_position()
    assert player_comp.position == 0
    assert player_comp.cash.balance == 3000 + c.CONST_GO_MONEY


def test_reset_player_position_and_move(player_comp):
    player_comp.reset_position()
    player_comp.move(10)
    assert player_comp.position == 10
    assert player_comp.cash.balance == 3000 + c.CONST_GO_MONEY
