import pytest

from src.game.place.railroad_card import RailroadCard
from src.game.place.property_set import PropertySet
from src.game.player import Player

from src.game.actions import Action as a


@pytest.fixture
def rail_card_simple():
    property_set = PropertySet(set_id=0)
    rail_card = RailroadCard(
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
    )
    property_set.add_property(rail_card)
    return rail_card


@pytest.fixture
def rail_card_diff_owners():
    property_set = PropertySet(set_id=0)
    rail_card_1 = RailroadCard(
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_character=1,
    )
    rail_card_2 = RailroadCard(
        name="Railroad 2",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_character=10,
    )
    property_set.add_property(rail_card_1)
    property_set.add_property(rail_card_2)
    return rail_card_1


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", character=0)
    return player


def test_rail_card_init(rail_card_simple):
    assert rail_card_simple.name == 'Railroad 1'
    assert rail_card_simple.price == 200
    assert rail_card_simple.rent == [25, 50, 100, 200]
    assert rail_card_simple.property_set.set_id == 0
    assert id(rail_card_simple.property_set.properties[0]) == id(rail_card_simple)
    assert rail_card_simple.mortgaged is False
    assert rail_card_simple.owner_character is None


def test_assign_owner(rail_card_simple):
    rail_card_simple.assign_owner(2)
    assert rail_card_simple.owner_character == 2


def test_assign_owner_one_owned_railroad(rail_card_diff_owners):
    rail_card_diff_owners.assign_owner(2)
    assert rail_card_diff_owners.property_set.count_owned(
        rail_card_diff_owners.owner_character
    ) == 1


def test_assign_owner_two_owned_railroad(rail_card_diff_owners):
    rail_card_diff_owners.assign_owner(10)
    assert rail_card_diff_owners.property_set.count_owned(
        rail_card_diff_owners.owner_character
    ) == 2


def test_compute_rent_one_owned_railroad(rail_card_diff_owners):
    assert rail_card_diff_owners.compute_rent() == 25


def test_compute_rent_two_owned_railroad(rail_card_diff_owners):
    rail_card_diff_owners.assign_owner(10)
    assert rail_card_diff_owners.compute_rent() == 50


def test_compute_rent_mortgaged_one_owned_railroad(rail_card_diff_owners):
    rail_card_diff_owners.mortgaged = True
    assert rail_card_diff_owners.compute_rent() == 0


def test_compute_rent_mortgaged_two_owned_railroad(rail_card_diff_owners):
    rail_card_diff_owners.assign_owner(10)
    rail_card_diff_owners.mortgaged = True
    assert rail_card_diff_owners.compute_rent() == 0


def test_mortgage(rail_card_diff_owners):
    rail_card_diff_owners.mortgage()
    assert rail_card_diff_owners.mortgaged is True


def test_mortgage_again(rail_card_diff_owners):
    rail_card_diff_owners.mortgage()
    with pytest.raises(ValueError, match='Property is already mortgaged'):
        rail_card_diff_owners.mortgage()


def test_mortgage_no_owner(rail_card_simple):
    with pytest.raises(ValueError, match="Property has no owner"):
        rail_card_simple.mortgage()


def test_trigger_unowned(rail_card_simple, player_simple):
    assert rail_card_simple.trigger(player_simple) == a.ASK_TO_BUY


def test_trigger_diff_owner(rail_card_diff_owners, player_simple):
    assert rail_card_diff_owners.trigger(player_simple) == a.CHARGE_RENT


def test_trigger_same_owner(rail_card_diff_owners, player_simple):
    player_simple.character = 1
    assert rail_card_diff_owners.trigger(player_simple) == a.NOTHING
