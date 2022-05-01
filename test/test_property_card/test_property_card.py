import pytest

from property_card import PropertyCard
from constants import CONST_HOUSE_LIMIT


@pytest.fixture
def prop_card_simple():
    property_card = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50
    )
    return property_card


@pytest.fixture
def prop_card_owner():
    property_card = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        owner_character=1,
    )
    return property_card


def test_property_card_init(prop_card_simple):
    assert prop_card_simple.name == 'Property 1'
    assert prop_card_simple.price == 60
    assert prop_card_simple.rent == [2, 10, 30, 90, 160, 250]
    assert prop_card_simple.price_of_house == 50
    assert prop_card_simple.price_of_hotel == 50
    assert prop_card_simple.no_of_houses == 0
    assert prop_card_simple.no_of_hotels == 0
    assert prop_card_simple.mortgaged is False
    assert prop_card_simple.owner_character is None


def test_assign_owner(prop_card_simple):
    prop_card_simple.assign_owner(2)
    assert prop_card_simple.owner_character == 2


def test_get_rent_without_monopoly(prop_card_simple):
    assert prop_card_simple.get_rent(monopoly=False) == 2


def test_get_rent_with_monopoly(prop_card_simple):
    assert prop_card_simple.get_rent(monopoly=True) == 4


def test_get_rent_some_houses_without_monopoly(prop_card_simple):
    prop_card_simple.no_of_houses = 2
    assert prop_card_simple.get_rent(monopoly=False) == 30


def test_get_rent_some_houses_with_monopoly(prop_card_simple):
    prop_card_simple.no_of_houses = 2
    assert prop_card_simple.get_rent(monopoly=True) == 30


def test_get_rent_full_houses_without_monopoly(prop_card_simple):
    prop_card_simple.no_of_houses = CONST_HOUSE_LIMIT
    assert prop_card_simple.get_rent(monopoly=False) == 160


def test_get_rent_full_houses_with_monopoly(prop_card_simple):
    prop_card_simple.no_of_houses = CONST_HOUSE_LIMIT
    assert prop_card_simple.get_rent(monopoly=True) == 160


def test_get_rent_hotel_without_monopoly(prop_card_simple):
    prop_card_simple.no_of_hotels = 1
    assert prop_card_simple.get_rent(monopoly=False) == 250


def test_get_rent_hotel_with_monopoly(prop_card_simple):
    prop_card_simple.no_of_hotels = 1
    assert prop_card_simple.get_rent(monopoly=True) == 250


def test_get_rent_mortgaged_without_monopoly(prop_card_owner):
    prop_card_owner.mortgaged = True
    assert prop_card_owner.get_rent(monopoly=False) == 0


def test_get_rent_mortgaged_with_monopoly(prop_card_owner):
    prop_card_owner.mortgaged = True
    assert prop_card_owner.get_rent(monopoly=True) == 0


def test_get_rent_mortgaged_with_house_or_hotel(prop_card_owner):
    prop_card_owner.mortgaged = True
    prop_card_owner.no_of_houses = 2
    assert prop_card_owner.get_rent(monopoly=False) == 0
    prop_card_owner.no_of_houses = CONST_HOUSE_LIMIT
    assert prop_card_owner.get_rent(monopoly=True) == 0
    prop_card_owner.no_of_hotels = 1
    assert prop_card_owner.get_rent(monopoly=True) == 0


def test_mortgage(prop_card_owner):
    prop_card_owner.mortgage()
    assert prop_card_owner.mortgaged is True
    assert prop_card_owner.get_rent(monopoly=False) == 0
    assert prop_card_owner.get_rent(monopoly=True) == 0


def test_mortgage_again(prop_card_owner):
    prop_card_owner.mortgage()
    with pytest.raises(ValueError, match='Property is already mortgaged'):
        prop_card_owner.mortgage()


def test_mortgage_no_owner(prop_card_simple):
    with pytest.raises(ValueError, match="Property has no owner"):
        prop_card_simple.mortgage()


def test_add_house(prop_card_simple):
    prop_card_simple.add_house()
    assert prop_card_simple.no_of_houses == 1


def test_add_house_full_house(prop_card_simple):
    prop_card_simple.no_of_houses = CONST_HOUSE_LIMIT
    with pytest.raises(ValueError, match="House limit reached"):
        prop_card_simple.add_house()


def test_add_house_mortgaged(prop_card_owner):
    prop_card_owner.mortgaged = True
    with pytest.raises(ValueError, match="Property is mortgaged"):
        prop_card_owner.add_house()


def test_add_hotel(prop_card_simple):
    prop_card_simple.no_of_houses = CONST_HOUSE_LIMIT
    prop_card_simple.add_hotel()
    assert prop_card_simple.no_of_hotels == 1
    assert prop_card_simple.no_of_houses == 0


def test_add_hotel_full_hotel(prop_card_simple):
    prop_card_simple.no_of_hotels = CONST_HOUSE_LIMIT
    with pytest.raises(ValueError, match="Not enough houses"):
        prop_card_simple.add_hotel()


def test_add_hotel_not_enough_houses(prop_card_simple):
    prop_card_simple.no_of_houses = CONST_HOUSE_LIMIT - 1
    with pytest.raises(ValueError, match="Not enough houses"):
        prop_card_simple.add_hotel()


def test_add_hotel_mortgaged(prop_card_owner):
    prop_card_owner.mortgaged = True
    with pytest.raises(ValueError, match="Property is mortgaged"):
        prop_card_owner.add_hotel()


def test_remove_house(prop_card_simple):
    prop_card_simple.no_of_houses = 1
    prop_card_simple.remove_house()
    assert prop_card_simple.no_of_houses == 0


def test_remove_house_empty(prop_card_simple):
    prop_card_simple.no_of_houses = 0
    with pytest.raises(ValueError, match="No houses to remove"):
        prop_card_simple.remove_house()


def test_remove_hotel(prop_card_simple):
    prop_card_simple.no_of_hotels = 1
    prop_card_simple.remove_hotel()
    assert prop_card_simple.no_of_hotels == 0
    assert prop_card_simple.no_of_houses == CONST_HOUSE_LIMIT


def test_remove_hotel_empty(prop_card_simple):
    prop_card_simple.no_of_hotels = 0
    with pytest.raises(ValueError, match="No hotels to remove"):
        prop_card_simple.remove_hotel()
