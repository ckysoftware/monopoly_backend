import constants as c
import pytest
from game import player, space
from game.actions import Action


@pytest.fixture
def prop_space_simple():
    property_set = space.PropertySet(id=0)
    property_space = space.PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_set.add_property(property_space)
    return property_space


@pytest.fixture
def prop_space_monopoly(prop_space_simple: space.PropertySpace):
    prop_space_simple.property_set.monopoly = True
    return prop_space_simple


@pytest.fixture
def prop_space_diff_owners():
    property_set = space.PropertySet(id=0)
    property_space_1 = space.PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=1,
    )
    property_space_2 = space.PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    return property_space_1


def test_property_space_init(prop_space_simple: space.PropertySpace):
    assert prop_space_simple.name == "Property 1"
    assert prop_space_simple.price == 60
    assert prop_space_simple.rent == [2, 10, 30, 90, 160, 250]
    assert prop_space_simple.price_of_house == 50
    assert prop_space_simple.price_of_hotel == 50
    assert prop_space_simple.property_set.id == 0
    assert id(prop_space_simple.property_set.properties[0]) == id(prop_space_simple)
    assert prop_space_simple.no_of_houses == 0
    assert prop_space_simple.no_of_hotels == 0
    assert prop_space_simple.mortgaged is False
    assert prop_space_simple.owner_uid is None


def test_assign_owner(prop_space_simple: space.PropertySpace):
    prop_space_simple.assign_owner(2)
    assert prop_space_simple.owner_uid == 2


def test_assign_owner_not_monopoly(prop_space_diff_owners: space.PropertySpace):
    prop_space_diff_owners.assign_owner(2)
    assert prop_space_diff_owners.property_set.monopoly is False


def test_assign_owner_is_monopoly(prop_space_diff_owners: space.PropertySpace):
    prop_space_diff_owners.assign_owner(10)
    assert prop_space_diff_owners.property_set.monopoly is True


def test_compute_rent_without_monopoly(prop_space_simple: space.PropertySpace):
    assert prop_space_simple.compute_rent() == 2


def test_compute_rent_with_monopoly(prop_space_monopoly: space.PropertySpace):
    assert prop_space_monopoly.compute_rent() == 4


def test_compute_rent_some_houses_without_monopoly(
    prop_space_simple: space.PropertySpace,
):
    prop_space_simple.no_of_houses = 2
    assert prop_space_simple.compute_rent() == 30


def test_compute_rent_some_houses_with_monopoly(
    prop_space_monopoly: space.PropertySpace,
):
    prop_space_monopoly.no_of_houses = 2
    assert prop_space_monopoly.compute_rent() == 30


def test_compute_rent_full_houses_without_monopoly(
    prop_space_simple: space.PropertySpace,
):
    prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT
    assert prop_space_simple.compute_rent() == 160


def test_compute_rent_full_houses_with_monopoly(
    prop_space_monopoly: space.PropertySpace,
):
    prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT
    assert prop_space_monopoly.compute_rent() == 160


def test_compute_rent_hotel_without_monopoly(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_hotels = 1
    assert prop_space_simple.compute_rent() == 250


def test_compute_rent_hotel_with_monopoly(prop_space_monopoly: space.PropertySpace):
    prop_space_monopoly.no_of_hotels = 1
    assert prop_space_monopoly.compute_rent() == 250


def test_compute_rent_mortgaged_without_monopoly(
    prop_space_simple: space.PropertySpace,
):
    prop_space_simple.mortgaged = True
    assert prop_space_simple.compute_rent() == 0


def test_compute_rent_mortgaged_with_monopoly(prop_space_monopoly: space.PropertySpace):
    prop_space_monopoly.mortgaged = True
    assert prop_space_monopoly.compute_rent() == 0


def test_compute_rent_mortgaged_with_house_or_hotel(
    prop_space_simple: space.PropertySpace,
):
    prop_space_simple.mortgaged = True
    prop_space_simple.no_of_houses = 2
    assert prop_space_simple.compute_rent() == 0
    prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT
    assert prop_space_simple.compute_rent() == 0
    prop_space_simple.no_of_hotels = 1
    assert prop_space_simple.compute_rent() == 0


def test_mortgage(prop_space_diff_owners: space.PropertySpace):
    prop_space_diff_owners.mortgage()
    assert prop_space_diff_owners.mortgaged is True


def test_mortgage_again(prop_space_diff_owners: space.PropertySpace):
    prop_space_diff_owners.mortgage()
    with pytest.raises(ValueError, match="Property is already mortgaged"):
        prop_space_diff_owners.mortgage()


def test_mortgage_no_owner(prop_space_simple: space.PropertySpace):
    with pytest.raises(ValueError, match="Property has no owner"):
        prop_space_simple.mortgage()


def test_add_house_in_monopoly(prop_space_monopoly: space.PropertySpace):
    prop_space_monopoly.add_house()
    assert prop_space_monopoly.no_of_houses == 1


def test_add_house_not_monopoly(prop_space_simple: space.PropertySpace):
    with pytest.raises(ValueError, match="Property is not in monopoly"):
        prop_space_simple.add_house()


def test_add_house_full_house(prop_space_monopoly: space.PropertySpace):
    prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT
    with pytest.raises(ValueError, match="House limit reached"):
        prop_space_monopoly.add_house()


def test_add_house_mortgaged(prop_space_monopoly: space.PropertySpace):
    prop_space_monopoly.mortgaged = True
    with pytest.raises(ValueError, match="Property is mortgaged"):
        prop_space_monopoly.add_house()


def test_add_hotel(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT
    prop_space_simple.add_hotel()
    assert prop_space_simple.no_of_hotels == 1
    assert prop_space_simple.no_of_houses == 0


def test_add_hotel_full_hotel(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_hotels = c.CONST_HOTEL_LIMIT
    with pytest.raises(ValueError, match="Hotel limit reached"):
        prop_space_simple.add_hotel()


def test_add_hotel_not_enough_houses(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT - 1
    with pytest.raises(ValueError, match="Not enough houses"):
        prop_space_simple.add_hotel()


def test_add_hotel_mortgaged(prop_space_simple: space.PropertySpace):
    prop_space_simple.mortgaged = True
    with pytest.raises(ValueError, match="Property is mortgaged"):
        prop_space_simple.add_hotel()


def test_remove_house(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_houses = 1
    prop_space_simple.remove_house()
    assert prop_space_simple.no_of_houses == 0


def test_remove_house_empty(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_houses = 0
    with pytest.raises(ValueError, match="No houses to remove"):
        prop_space_simple.remove_house()


def test_remove_hotel(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_hotels = 1
    prop_space_simple.remove_hotel()
    assert prop_space_simple.no_of_hotels == 0
    assert prop_space_simple.no_of_houses == c.CONST_HOUSE_LIMIT


def test_remove_hotel_empty(prop_space_simple: space.PropertySpace):
    prop_space_simple.no_of_hotels = 0
    with pytest.raises(ValueError, match="No hotels to remove"):
        prop_space_simple.remove_hotel()


def test_trigger_unowned(
    prop_space_simple: space.PropertySpace, player_simple: player.Player
):
    assert prop_space_simple.trigger(player_simple) == Action.ASK_TO_BUY


def test_trigger_diff_owner(
    prop_space_diff_owners: space.PropertySpace, player_simple: player.Player
):
    assert prop_space_diff_owners.trigger(player_simple) == Action.PAY_RENT


def test_trigger_same_owner(
    prop_space_diff_owners: space.PropertySpace, player_simple: player.Player
):
    player_simple.uid = 1
    assert prop_space_diff_owners.trigger(player_simple) == Action.NOTHING
