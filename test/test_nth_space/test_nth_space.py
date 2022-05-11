import constants as c
import pytest
from game.actions import Action
from game.player import Player
from game.space import NthSpace


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


@pytest.fixture
def nth_space_simple():
    nth_space = NthSpace(name="Go")
    return nth_space


def test_nth_space_init(nth_space_simple):
    assert nth_space_simple.name == "Go"


def test_nth_space_trigger(nth_space_simple, player_simple):
    assert nth_space_simple.trigger(player_simple) == Action.NOTHING
