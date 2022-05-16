import constants as c
import pytest
from game import space
from game.actions import Action
from game.player import Player


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


@pytest.fixture
def jail_space_simple():
    jail_space = space.JailSpace(name="Go")
    return jail_space


def test_nth_space_init(jail_space_simple):
    assert jail_space_simple.name == "Go"


def test_nth_space_trigger(jail_space_simple, player_simple):
    assert jail_space_simple.trigger(player_simple) == Action.SEND_TO_JAIL
