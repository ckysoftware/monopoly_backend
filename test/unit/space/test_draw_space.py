import constants as c
import pytest
from game import enum_types, player, space
from game.actions import Action


@pytest.fixture
def player_simple():
    player_simple = player.Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player_simple


@pytest.fixture
def draw_space_chance_card():
    draw_space_chance_card = space.DrawSpace(
        name="Chance Card", deck_type=enum_types.DeckType.CHANCE
    )
    return draw_space_chance_card


@pytest.fixture
def draw_space_cc_card():
    draw_space_cc_card = space.DrawSpace(
        name="Community Chest Card", deck_type=enum_types.DeckType.CC
    )
    return draw_space_cc_card


def test_draw_space_chance_card_init(draw_space_chance_card: space.DrawSpace):
    assert draw_space_chance_card.name == "Chance Card"
    assert draw_space_chance_card.deck_type == enum_types.DeckType.CHANCE


def test_draw_space_cc_card_init(draw_space_cc_card: space.DrawSpace):
    assert draw_space_cc_card.name == "Community Chest Card"
    assert draw_space_cc_card.deck_type == enum_types.DeckType.CC


def test_draw_space_chance_card_trigger(
    draw_space_chance_card: space.DrawSpace, player_simple: player.Player
):
    assert (
        draw_space_chance_card.trigger(player=player_simple) == Action.DRAW_CHANCE_CARD
    )


def test_draw_space_cc_card_trigger(
    draw_space_cc_card: space.DrawSpace, player_simple: player.Player
):
    assert draw_space_cc_card.trigger(player=player_simple) == Action.DRAW_CC_CARD


def test_draw_space_unknown_card_init(player_simple: player.Player):
    unknown = space.DrawSpace(
        name="Unknown", deck_type="unknown"
    )  # pyright: reportGeneralTypeIssues=false
    with pytest.raises(ValueError, match="Unknown deck type."):
        unknown.trigger(player=player_simple)
