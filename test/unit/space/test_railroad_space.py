import pytest
from game import player, space
from game.actions import Action


@pytest.fixture
def rail_space_simple():
    property_set = space.PropertySet(id=0)
    rail_space = space.RailroadSpace(
        id=1,
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
    )
    property_set.add_property(rail_space)
    return rail_space


@pytest.fixture
def rail_space_diff_owners():
    property_set = space.PropertySet(id=0)
    rail_space_1 = space.RailroadSpace(
        id=1,
        name="Railroad 1",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_uid=1,
    )
    rail_space_2 = space.RailroadSpace(
        id=2,
        name="Railroad 2",
        price=200,
        rent=[25, 50, 100, 200],
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(rail_space_1)
    property_set.add_property(rail_space_2)
    return rail_space_1


def test_rail_space_init(rail_space_simple: space.RailroadSpace):
    assert rail_space_simple.name == "Railroad 1"
    assert rail_space_simple.price == 200
    assert rail_space_simple.rent == [25, 50, 100, 200]
    assert rail_space_simple.property_set.id == 0
    assert id(rail_space_simple.property_set.properties[0]) == id(rail_space_simple)
    assert rail_space_simple.mortgaged is False
    assert rail_space_simple.owner_uid is None


def test_assign_owner(rail_space_simple: space.RailroadSpace):
    rail_space_simple.assign_owner(2)
    assert rail_space_simple.owner_uid == 2


def test_assign_owner_one_owned_railroad(rail_space_diff_owners: space.RailroadSpace):
    rail_space_diff_owners.assign_owner(2)
    assert rail_space_diff_owners.owner_uid is not None
    assert (
        rail_space_diff_owners.property_set.count_owned(
            rail_space_diff_owners.owner_uid
        )
        == 1
    )


def test_assign_owner_two_owned_railroad(rail_space_diff_owners: space.RailroadSpace):
    rail_space_diff_owners.assign_owner(10)
    assert rail_space_diff_owners.owner_uid is not None
    assert (
        rail_space_diff_owners.property_set.count_owned(
            rail_space_diff_owners.owner_uid
        )
        == 2
    )


def test_compute_rent_one_owned_railroad(rail_space_diff_owners: space.RailroadSpace):
    assert rail_space_diff_owners.compute_rent() == 25


def test_compute_rent_two_owned_railroad(rail_space_diff_owners: space.RailroadSpace):
    rail_space_diff_owners.assign_owner(10)
    assert rail_space_diff_owners.compute_rent() == 50


def test_compute_rent_mortgaged_one_owned_railroad(
    rail_space_diff_owners: space.RailroadSpace,
):
    rail_space_diff_owners.mortgaged = True
    assert rail_space_diff_owners.compute_rent() == 0


def test_compute_rent_mortgaged_two_owned_railroad(
    rail_space_diff_owners: space.RailroadSpace,
):
    rail_space_diff_owners.assign_owner(10)
    rail_space_diff_owners.mortgaged = True
    assert rail_space_diff_owners.compute_rent() == 0


def test_mortgage(rail_space_diff_owners: space.RailroadSpace):
    rail_space_diff_owners.mortgage()
    assert rail_space_diff_owners.mortgaged is True


def test_mortgage_again(rail_space_diff_owners: space.RailroadSpace):
    rail_space_diff_owners.mortgage()
    with pytest.raises(ValueError, match="Property is already mortgaged"):
        rail_space_diff_owners.mortgage()


def test_mortgage_no_owner(rail_space_simple: space.RailroadSpace):
    with pytest.raises(ValueError, match="Property has no owner"):
        rail_space_simple.mortgage()


def test_trigger_unowned(
    rail_space_simple: space.RailroadSpace, player_simple: player.Player
):
    assert rail_space_simple.trigger(player_simple) == Action.ASK_TO_BUY


def test_trigger_diff_owner(
    rail_space_diff_owners: space.RailroadSpace, player_simple: player.Player
):
    assert rail_space_diff_owners.trigger(player_simple) == Action.PAY_RENT


def test_trigger_same_owner(
    rail_space_diff_owners: space.RailroadSpace, player_simple: player.Player
):
    player_simple.uid = 1
    assert rail_space_diff_owners.trigger(player_simple) == Action.NOTHING
