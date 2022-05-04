import pytest

from src.game.place.property_card import PropertyCard
from src.game.place.property_set import PropertySet


@pytest.fixture
def prop_set_simple():
    property_set = PropertySet(set_id=2)
    property_card = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
    )
    property_set.add_property(property_card)
    return property_set


@pytest.fixture
def prop_set_monopoly():
    property_set = PropertySet(set_id=2)
    property_card_1 = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_character=1,
    )
    property_card_2 = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_character=1,
    )
    property_set.add_property(property_card_1)
    property_set.add_property(property_card_2)
    property_set.monopoly = True
    return property_set


def test_property_set_init(prop_set_simple):
    assert prop_set_simple.set_id == 2
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
    prop_set_monopoly.properties[0].owner_character = 0
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False


def test_property_set_update_monopoly_has_unowned(prop_set_monopoly):
    prop_set_monopoly.properties[-1].owner_character = None
    prop_set_monopoly.update_monopoly()
    assert prop_set_monopoly.monopoly is False
