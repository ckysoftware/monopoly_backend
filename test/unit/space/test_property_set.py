import constants as c
import pytest
from game import space


@pytest.fixture
def prop_set_simple():
    property_set = space.PropertySet(id=2)
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
    return property_set


@pytest.fixture
def prop_set_monopoly(prop_set_simple: space.PropertySet):
    property_space_2 = space.PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=prop_set_simple,
        owner_uid=1,
    )
    prop_set_simple.properties[0].owner_uid = 1
    prop_set_simple.add_property(property_space_2)
    prop_set_simple.monopoly = True
    return prop_set_simple


@pytest.fixture
def prop_set_four_unowned(prop_set_simple: space.PropertySet):
    property_space_2 = space.PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=prop_set_simple,
    )
    property_space_3 = space.PropertySpace(
        name="Property 3",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=prop_set_simple,
    )
    property_space_4 = space.PropertySpace(
        name="Property 4",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=prop_set_simple,
    )
    prop_set_simple.add_property(property_space_2)
    prop_set_simple.add_property(property_space_3)
    prop_set_simple.add_property(property_space_4)
    return prop_set_simple


def test_property_set_init(prop_set_simple: space.PropertySet):
    assert prop_set_simple.id == 2
    assert len(prop_set_simple.properties) == 1
    assert id(prop_set_simple.properties[0].property_set) == id(prop_set_simple)
    assert prop_set_simple.monopoly is False


def test_property_set_empty(prop_set_monopoly: space.PropertySet):
    prop_set_monopoly.properties = []
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_update_is_monopoly(prop_set_monopoly: space.PropertySet):
    prop_set_monopoly.monopoly = False
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is True


def test_property_set_update_not_monopoly(prop_set_monopoly: space.PropertySet):
    prop_set_monopoly.properties[0].owner_uid = 0
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_update_monopoly_has_unowned(prop_set_monopoly: space.PropertySet):
    prop_set_monopoly.properties[-1].owner_uid = None
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_count_owner_unowned(prop_set_four_unowned: space.PropertySet):
    assert prop_set_four_unowned.count_owned(1) == 0


def test_property_set_count_owner_one_with_unowned(
    prop_set_four_unowned: space.PropertySet,
):
    prop_set_four_unowned.properties[2].owner_uid = 1
    assert prop_set_four_unowned.count_owned(1) == 1


def test_property_set_count_owner_unowned_with_other_owned(
    prop_set_four_unowned: space.PropertySet,
):
    prop_set_four_unowned.properties[2].owner_uid = 1
    prop_set_four_unowned.properties[3].owner_uid = 10
    assert prop_set_four_unowned.count_owned(5) == 0


def test_property_set_count_owner_three_owned(prop_set_four_unowned: space.PropertySet):
    prop_set_four_unowned.properties[0].owner_uid = 1
    prop_set_four_unowned.properties[2].owner_uid = 1
    prop_set_four_unowned.properties[3].owner_uid = 1
    assert prop_set_four_unowned.count_owned(1) == 3
