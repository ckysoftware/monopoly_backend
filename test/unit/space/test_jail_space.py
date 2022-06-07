import pytest
from game import player, space
from game.actions import Action


@pytest.fixture
def jail_space_simple():
    jail_space = space.JailSpace(name="Go")
    return jail_space


def test_nth_space_init(jail_space_simple: player.Player):
    assert jail_space_simple.name == "Go"


def test_nth_space_trigger(
    jail_space_simple: space.JailSpace, player_simple: player.Player
):
    assert jail_space_simple.trigger(player_simple) == Action.SEND_TO_JAIL
