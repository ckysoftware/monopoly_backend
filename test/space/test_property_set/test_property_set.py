import constants as c
import pytest
from game.space import PropertySpace, PropertySet


@pytest.fixture
def prop_set_simple():
    property_set = PropertySet(id=2)
    property_space = PropertySpace(
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
    return property_set


@pytest.fixture
def prop_set_monopoly():
    property_set = PropertySet(id=2)
    property_space_1 = PropertySpace(
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
    property_space_2 = PropertySpace(
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
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    property_set.monopoly = True
    return property_set


@pytest.fixture
def prop_set_four_unowned():
    property_set = PropertySet(id=2)
    property_space_1 = PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_space_2 = PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_space_3 = PropertySpace(
        name="Property 3",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_space_4 = PropertySpace(
        name="Property 4",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    property_set.add_property(property_space_3)
    property_set.add_property(property_space_4)
    return property_set


def test_property_set_init(prop_set_simple):
    assert prop_set_simple.id == 2
    assert len(prop_set_simple.properties) == 1
    assert id(prop_set_simple.properties[0].property_set) == id(prop_set_simple)
    assert prop_set_simple.monopoly is False


def test_property_set_empty(prop_set_monopoly):
    prop_set_monopoly.properties = []
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_update_is_monopoly(prop_set_monopoly):
    prop_set_monopoly.monopoly = False
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is True


def test_property_set_update_not_monopoly(prop_set_monopoly):
    prop_set_monopoly.properties[0].owner_uid = 0
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_update_monopoly_has_unowned(prop_set_monopoly):
    prop_set_monopoly.properties[-1].owner_uid = None
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_count_owner_unowned(prop_set_four_unowned):
    assert prop_set_four_unowned.count_owned(1) == 0


def test_property_set_count_owner_one_with_unowned(prop_set_four_unowned):
    prop_set_four_unowned.properties[2].owner_uid = 1
    assert prop_set_four_unowned.count_owned(1) == 1


def test_property_set_count_owner_unowned_with_other_owned(prop_set_four_unowned):
    prop_set_four_unowned.properties[2].owner_uid = 1
    prop_set_four_unowned.properties[3].owner_uid = 10
    assert prop_set_four_unowned.count_owned(5) == 0


def test_property_set_count_owner_three_owned(prop_set_four_unowned):
    prop_set_four_unowned.properties[0].owner_uid = 1
    prop_set_four_unowned.properties[2].owner_uid = 1
    prop_set_four_unowned.properties[3].owner_uid = 1
    assert prop_set_four_unowned.count_owned(1) == 3
