import pytest
from game import card
from game.actions import Action


@pytest.fixture
def chance_card_simple():
    chance_card = card.ChanceCard(
        id=0,
        description="Advance to Boardwalk",
        action=Action.SEND_TO_BOARDWALK,
        ownable=False,
    )
    return chance_card


@pytest.fixture
def chance_card_ownable():
    ownable_chance_card = card.ChanceCard(
        id=8,
        description="Get out of Jail Free. This card may be kept until needed, or traded/sold.",
        action=Action.COLLECT_JAIL_CARD,
        ownable=True,
    )
    return ownable_chance_card


def test_chance_card_simple_init(chance_card_simple: card.ChanceCard):
    assert chance_card_simple.id == 0
    assert chance_card_simple.description == "Advance to Boardwalk"
    assert chance_card_simple.action == Action.SEND_TO_BOARDWALK
    assert chance_card_simple.ownable is False


def test_chance_card_simple_trigger(chance_card_simple: card.ChanceCard):
    assert chance_card_simple.trigger() == Action.SEND_TO_BOARDWALK


def test_chance_card_ownable_init(chance_card_ownable: card.ChanceCard):
    assert chance_card_ownable.id == 8
    assert (
        chance_card_ownable.description
        == "Get out of Jail Free. This card may be kept until needed, or traded/sold."
    )
    assert chance_card_ownable.action == Action.COLLECT_JAIL_CARD
    assert chance_card_ownable.ownable is True


def test_chance_card_ownable_trigger(chance_card_ownable: card.ChanceCard):
    assert chance_card_ownable.trigger() == Action.COLLECT_JAIL_CARD
