import pytest
from game import player, space
from game.actions import Action


@pytest.fixture
def nth_space_simple():
    nth_space = space.NthSpace(name="Go")
    return nth_space


def test_nth_space_init(nth_space_simple: space.NthSpace):
    assert nth_space_simple.name == "Go"


def test_nth_space_trigger(
    nth_space_simple: space.NthSpace, player_simple: player.Player
):
    assert nth_space_simple.trigger(player_simple) == Action.NOTHING
