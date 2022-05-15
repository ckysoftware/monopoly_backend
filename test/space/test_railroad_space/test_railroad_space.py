import constants as c
import pytest
from game.actions import Action
from game.player import Player
from game.space import PropertySet, RailroadSpace


@pytest.fixture
def rail_space_simple():
    property_set = PropertySet(id=0)
    rail_space = RailroadSpace(
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
    )
    property_set.add_property(rail_space)
    return rail_space


@pytest.fixture
def rail_space_diff_owners():
    property_set = PropertySet(id=0)
    rail_space_1 = RailroadSpace(
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_uid=1,
    )
    rail_space_2 = RailroadSpace(
        name="Railroad 2",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(rail_space_1)
    property_set.add_property(rail_space_2)
    return rail_space_1


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


def test_rail_space_init(rail_space_simple):
    assert rail_space_simple.name == "Railroad 1"
    assert rail_space_simple.price == 200
    assert rail_space_simple.rent == [25, 50, 100, 200]
    assert rail_space_simple.property_set.id == 0
    assert id(rail_space_simple.property_set.properties[0]) == id(rail_space_simple)
    assert rail_space_simple.mortgaged is False
    assert rail_space_simple.owner_uid is None


def test_assign_owner(rail_space_simple):
    rail_space_simple.assign_owner(2)
    assert rail_space_simple.owner_uid == 2


def test_assign_owner_one_owned_railroad(rail_space_diff_owners):
    rail_space_diff_owners.assign_owner(2)
    assert (
        rail_space_diff_owners.property_set.count_owned(
            rail_space_diff_owners.owner_uid
        )
        == 1
    )


def test_assign_owner_two_owned_railroad(rail_space_diff_owners):
    rail_space_diff_owners.assign_owner(10)
    assert (
        rail_space_diff_owners.property_set.count_owned(
            rail_space_diff_owners.owner_uid
        )
        == 2
    )


def test_compute_rent_one_owned_railroad(rail_space_diff_owners):
    assert rail_space_diff_owners.compute_rent() == 25


def test_compute_rent_two_owned_railroad(rail_space_diff_owners):
    rail_space_diff_owners.assign_owner(10)
    assert rail_space_diff_owners.compute_rent() == 50


def test_compute_rent_mortgaged_one_owned_railroad(rail_space_diff_owners):
    rail_space_diff_owners.mortgaged = True
    assert rail_space_diff_owners.compute_rent() == 0


def test_compute_rent_mortgaged_two_owned_railroad(rail_space_diff_owners):
    rail_space_diff_owners.assign_owner(10)
    rail_space_diff_owners.mortgaged = True
    assert rail_space_diff_owners.compute_rent() == 0


def test_mortgage(rail_space_diff_owners):
    rail_space_diff_owners.mortgage()
    assert rail_space_diff_owners.mortgaged is True


def test_mortgage_again(rail_space_diff_owners):
    rail_space_diff_owners.mortgage()
    with pytest.raises(ValueError, match="Property is already mortgaged"):
        rail_space_diff_owners.mortgage()


def test_mortgage_no_owner(rail_space_simple):
    with pytest.raises(ValueError, match="Property has no owner"):
        rail_space_simple.mortgage()


def test_trigger_unowned(rail_space_simple, player_simple):
    assert rail_space_simple.trigger(player_simple) == Action.ASK_TO_BUY


def test_trigger_diff_owner(rail_space_diff_owners, player_simple):
    assert rail_space_diff_owners.trigger(player_simple) == Action.PAY_RENT


def test_trigger_same_owner(rail_space_diff_owners, player_simple):
    player_simple.uid = 1
    assert rail_space_diff_owners.trigger(player_simple) == Action.NOTHING
