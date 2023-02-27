import pytest

import constants as c
from game import player, space
from game.actions import Action


@pytest.fixture
def prop_space_simple():
    property_set = space.PropertySet(id=0)
    property_space = space.PropertySpace(
        id=1,
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
        id=1,
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
        id=2,
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


@pytest.fixture
def prop_space_multi_monopoly(prop_space_diff_owners: space.PropertySpace):
    prop_space_diff_owners.property_set.properties[1].assign_owner(1)
    return prop_space_diff_owners


def test_property_space_init(prop_space_simple: space.PropertySpace):
    assert prop_space_simple.name == "Property 1"
    assert prop_space_simple.price == 60
    assert prop_space_simple.rent == [2, 10, 30, 90, 160, 250]
    assert prop_space_simple.price_of_house == 50
    assert prop_space_simple.price_of_hotel == 50
    assert prop_space_simple.property_set.id == prop_space_simple.property_set_id == 0
    assert id(prop_space_simple.property_set.properties[0]) == id(prop_space_simple)
    assert prop_space_simple.no_of_houses == 0
    assert prop_space_simple.no_of_hotels == 0
    assert prop_space_simple.mortgaged is False
    assert prop_space_simple.owner_uid is None


class TestAssignOwner:
    def test_assign_owner(self, prop_space_simple: space.PropertySpace):
        prop_space_simple.assign_owner(2)
        assert prop_space_simple.owner_uid == 2

    def test_assign_owner_not_monopoly(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        prop_space_diff_owners.assign_owner(2)
        assert prop_space_diff_owners.property_set.monopoly is False

    def test_assign_owner_is_monopoly(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        prop_space_diff_owners.assign_owner(10)
        assert prop_space_diff_owners.property_set.monopoly is True


class TestComputeRent:
    def test_compute_rent_without_monopoly(
        self, prop_space_simple: space.PropertySpace
    ):
        assert prop_space_simple.compute_rent() == 2

    def test_compute_rent_with_monopoly(self, prop_space_monopoly: space.PropertySpace):
        assert prop_space_monopoly.compute_rent() == 4

    def test_compute_rent_some_houses_without_monopoly(
        self,
        prop_space_simple: space.PropertySpace,
    ):
        prop_space_simple.no_of_houses = 2
        assert prop_space_simple.compute_rent() == 30

    def test_compute_rent_some_houses_with_monopoly(
        self,
        prop_space_monopoly: space.PropertySpace,
    ):
        prop_space_monopoly.no_of_houses = 2
        assert prop_space_monopoly.compute_rent() == 30

    def test_compute_rent_full_houses_without_monopoly(
        self,
        prop_space_simple: space.PropertySpace,
    ):
        prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT
        assert prop_space_simple.compute_rent() == 160

    def test_compute_rent_full_houses_with_monopoly(
        self,
        prop_space_monopoly: space.PropertySpace,
    ):
        prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT
        assert prop_space_monopoly.compute_rent() == 160

    def test_compute_rent_hotel_without_monopoly(
        self,
        prop_space_simple: space.PropertySpace,
    ):
        prop_space_simple.no_of_hotels = 1
        assert prop_space_simple.compute_rent() == 250

    def test_compute_rent_hotel_with_monopoly(
        self, prop_space_monopoly: space.PropertySpace
    ):
        prop_space_monopoly.no_of_hotels = 1
        assert prop_space_monopoly.compute_rent() == 250

    def test_compute_rent_mortgaged_without_monopoly(
        self,
        prop_space_simple: space.PropertySpace,
    ):
        prop_space_simple.mortgaged = True
        assert prop_space_simple.compute_rent() == 0

    def test_compute_rent_mortgaged_with_monopoly(
        self,
        prop_space_monopoly: space.PropertySpace,
    ):
        prop_space_monopoly.mortgaged = True
        assert prop_space_monopoly.compute_rent() == 0

    def test_compute_rent_mortgaged_with_house_or_hotel(
        self,
        prop_space_simple: space.PropertySpace,
    ):
        prop_space_simple.mortgaged = True
        prop_space_simple.no_of_houses = 2
        assert prop_space_simple.compute_rent() == 0
        prop_space_simple.no_of_houses = c.CONST_HOUSE_LIMIT
        assert prop_space_simple.compute_rent() == 0
        prop_space_simple.no_of_hotels = 1
        assert prop_space_simple.compute_rent() == 0


class TestMortgage:
    def test_mortgage(self, prop_space_diff_owners: space.PropertySpace):
        mortgage_value = prop_space_diff_owners.mortgage()
        assert prop_space_diff_owners.mortgaged is True
        assert mortgage_value == prop_space_diff_owners.mortgage_value

    def test_mortgage_again(self, prop_space_diff_owners: space.PropertySpace):
        prop_space_diff_owners.mortgage()
        with pytest.raises(ValueError, match="Property is already mortgaged"):
            prop_space_diff_owners.mortgage()

    def test_mortgage_no_owner(self, prop_space_simple: space.PropertySpace):
        with pytest.raises(ValueError, match="Property has no owner"):
            prop_space_simple.mortgage()

    def test_mortgage_this_property_has_house_or_hotel(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        prop_space_diff_owners.property_set.properties[1].assign_owner(1)
        prop_space_diff_owners.no_of_hotels = 1
        with pytest.raises(ValueError, match="Property set has houses or hotels"):
            prop_space_diff_owners.mortgage()

    def test_mortgage_other_properties_have_house_or_hotel(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        other_property = prop_space_diff_owners.property_set.properties[1]
        assert isinstance(other_property, space.PropertySpace)
        other_property.assign_owner(1)
        other_property.add_house()
        with pytest.raises(ValueError, match="Property set has houses or hotels"):
            prop_space_diff_owners.mortgage()

    def test_allow_mortgage(self, prop_space_diff_owners: space.PropertySpace):
        assert prop_space_diff_owners.allow_mortgage() is True

    def test_allow_mortgage_already_mortgaged(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        prop_space_diff_owners.mortgage()
        assert prop_space_diff_owners.allow_mortgage() is False

    def test_allow_mortgage_no_owner(self, prop_space_simple: space.PropertySpace):
        assert prop_space_simple.allow_mortgage() is False

    def test_allow_mortgage_this_property_has_house_or_hotel(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        prop_space_diff_owners.property_set.properties[1].assign_owner(1)
        prop_space_diff_owners.no_of_hotels = 1
        assert prop_space_diff_owners.allow_mortgage() is False

    def test_allow_mortgage_other_properties_have_house_or_hotel(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        other_property = prop_space_diff_owners.property_set.properties[1]
        assert isinstance(other_property, space.PropertySpace)
        other_property.assign_owner(1)
        other_property.add_house()
        assert prop_space_diff_owners.allow_mortgage() is False

    def test_unmortgage(self, prop_space_diff_owners: space.PropertySpace):
        mortgage_value = prop_space_diff_owners.mortgage()
        unmortgage_value = prop_space_diff_owners.unmortgage()
        assert unmortgage_value == mortgage_value * 1.1
        assert isinstance(unmortgage_value, int)

    def test_unmortgage_not_mortgaged(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        with pytest.raises(ValueError, match="Property is not mortgaged"):
            _unmortgage_value = prop_space_diff_owners.unmortgage()

    def test_allow_unmortgage(self, prop_space_diff_owners: space.PropertySpace):
        _mortgage_value = prop_space_diff_owners.mortgage()
        assert prop_space_diff_owners.allow_unmortgage() is True

    def test_allow_unmortgage_not_mortgaged(
        self, prop_space_diff_owners: space.PropertySpace
    ):
        assert prop_space_diff_owners.allow_unmortgage() is False

    def test_get_mortgage_value(self, prop_space_simple: space.PropertySpace):
        assert prop_space_simple.mortgage_value == prop_space_simple.price // 2


class TestBuildHouseOrHotel:
    def test_add_house_in_monopoly(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.add_house()
        assert prop_space_monopoly.no_of_houses == 1

    def test_add_house_not_monopoly(self, prop_space_simple: space.PropertySpace):
        with pytest.raises(ValueError, match="Property is not in monopoly"):
            prop_space_simple.add_house()

    def test_add_house_full_house(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT
        with pytest.raises(ValueError, match="House limit reached"):
            prop_space_monopoly.add_house()

    def test_add_house_mortgaged(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.mortgaged = True
        with pytest.raises(ValueError, match="Property is mortgaged"):
            prop_space_monopoly.add_house()

    def test_add_house_same_num(self, prop_space_multi_monopoly: space.PropertySpace):
        prop_space_multi_monopoly.add_house()
        assert prop_space_multi_monopoly.no_of_houses == 1

    def test_add_house_one_less(self, prop_space_multi_monopoly: space.PropertySpace):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_houses = 1  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.add_house()
        assert prop_space_multi_monopoly.no_of_houses == 1

    def test_add_house_one_more(self, prop_space_multi_monopoly: space.PropertySpace):
        prop_space_multi_monopoly.no_of_houses = 1
        with pytest.raises(
            ValueError, match="Houses are not evenly distributed in the property set"
        ):
            prop_space_multi_monopoly.add_house()

    def test_add_hotel_in_monopoly(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = prop_space_monopoly.HOUSE_LIMIT
        prop_space_monopoly.add_hotel()
        assert prop_space_monopoly.no_of_hotels == 1
        assert prop_space_monopoly.no_of_houses == 0

    def test_add_hotel_not_monopoly(self, prop_space_simple: space.PropertySpace):
        prop_space_simple.no_of_houses = prop_space_simple.HOUSE_LIMIT
        with pytest.raises(ValueError, match="Property is not in monopoly"):
            prop_space_simple.add_hotel()

    def test_add_hotel_full_hotel(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = c.CONST_HOTEL_LIMIT
        with pytest.raises(ValueError, match="Hotel limit reached"):
            prop_space_monopoly.add_hotel()

    def test_add_hotel_not_enough_houses(
        self, prop_space_monopoly: space.PropertySpace
    ):
        prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT - 1
        with pytest.raises(ValueError, match="Not enough houses"):
            prop_space_monopoly.add_hotel()

    def test_add_hotel_mortgaged(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.mortgaged = True
        with pytest.raises(ValueError, match="Property is mortgaged"):
            prop_space_monopoly.add_hotel()

    def test_add_hotel_same_num(self, prop_space_multi_monopoly: space.PropertySpace):
        for property_ in prop_space_multi_monopoly.property_set.properties:
            assert isinstance(property_, space.PropertySpace)
            property_.no_of_houses = property_.HOUSE_LIMIT
        prop_space_multi_monopoly.add_hotel()
        assert prop_space_multi_monopoly.no_of_hotels == 1

    def test_add_hotel_one_less(self, prop_space_multi_monopoly: space.PropertySpace):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_hotels = 1  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        prop_space_multi_monopoly.add_hotel()
        assert prop_space_multi_monopoly.no_of_hotels == 1

    def test_add_hotel_one_more(self, prop_space_multi_monopoly: space.PropertySpace):
        prop_space_multi_monopoly.property_set.properties[1].no_of_houses = (
            prop_space_multi_monopoly.HOUSE_LIMIT - 1
        )  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        with pytest.raises(
            ValueError, match="Houses are not evenly distributed in the property set"
        ):
            prop_space_multi_monopoly.add_hotel()

    def test_allow_add_house_in_monopoly(
        self, prop_space_monopoly: space.PropertySpace
    ):
        assert prop_space_monopoly.allow_add_house() is True

    def test_allow_add_house_not_monopoly(self, prop_space_simple: space.PropertySpace):
        assert prop_space_simple.allow_add_house() is False

    def test_allow_add_house_full_house(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT
        assert prop_space_monopoly.allow_add_house() is False

    def test_allow_add_house_mortgaged(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.mortgaged = True
        assert prop_space_monopoly.allow_add_house() is False

    def test_allow_add_house_same_num(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        assert prop_space_multi_monopoly.allow_add_house() is True

    def test_allow_add_house_one_less(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[1].no_of_houses = 1
        assert prop_space_multi_monopoly.allow_add_house() is True

    def test_allow_add_house_one_more(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.no_of_houses = 1
        assert prop_space_multi_monopoly.allow_add_house() is False

    def test_allow_add_hotel_in_monopoly(
        self, prop_space_monopoly: space.PropertySpace
    ):
        prop_space_monopoly.no_of_houses = prop_space_monopoly.HOUSE_LIMIT
        assert prop_space_monopoly.allow_add_hotel() is True

    def test_allow_add_hotel_not_monopoly(self, prop_space_simple: space.PropertySpace):
        prop_space_simple.no_of_houses = prop_space_simple.HOUSE_LIMIT
        assert prop_space_simple.allow_add_hotel() is False

    def test_allow_add_hotel_full_hotel(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = c.CONST_HOTEL_LIMIT
        assert prop_space_monopoly.allow_add_hotel() is False

    def test_allow_add_hotel_not_enough_houses(
        self, prop_space_monopoly: space.PropertySpace
    ):
        prop_space_monopoly.no_of_houses = c.CONST_HOUSE_LIMIT - 1
        assert prop_space_monopoly.allow_add_hotel() is False

    def test_allow_add_hotel_mortgaged(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.mortgaged = True
        assert prop_space_monopoly.allow_add_hotel() is False

    def test_allow_add_hotel_same_num(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        for property_ in prop_space_multi_monopoly.property_set.properties:
            assert isinstance(property_, space.PropertySpace)
            property_.no_of_houses = property_.HOUSE_LIMIT
        assert prop_space_multi_monopoly.allow_add_hotel() is True

    def test_allow_add_hotel_one_less(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[1].no_of_hotels = 1
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        assert prop_space_multi_monopoly.allow_add_hotel() is True

    def test_allow_add_hotel_one_more(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[1].no_of_houses = (
            prop_space_multi_monopoly.HOUSE_LIMIT - 1
        )
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        assert prop_space_multi_monopoly.allow_add_hotel() is False

    def test_remove_house(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = 1
        prop_space_monopoly.remove_house()
        assert prop_space_monopoly.no_of_houses == 0

    def test_remove_house_empty(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = 0
        with pytest.raises(ValueError, match="No houses to remove"):
            prop_space_monopoly.remove_house()

    def test_remove_house_same_num(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        for property_ in prop_space_multi_monopoly.property_set.properties:
            assert isinstance(property_, space.PropertySpace)
            property_.no_of_houses = 1
        prop_space_multi_monopoly.remove_house()
        assert prop_space_multi_monopoly.no_of_houses == 0

    def test_remove_house_one_less_with_hotel(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_hotels = 1  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        with pytest.raises(
            ValueError, match="Houses are not evenly distributed in the property set"
        ):
            prop_space_multi_monopoly.remove_house()

    def test_remove_house_one_less_without_hotel(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_houses = 3  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = 2
        with pytest.raises(
            ValueError, match="Houses are not evenly distributed in the property set"
        ):
            prop_space_multi_monopoly.remove_house()

    def test_remove_house_one_more(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_houses = 2  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = 3
        prop_space_multi_monopoly.remove_house()
        assert prop_space_multi_monopoly.no_of_houses == 2

    def test_remove_hotel(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = 1
        prop_space_monopoly.remove_hotel()
        assert prop_space_monopoly.no_of_hotels == 0
        assert prop_space_monopoly.no_of_houses == c.CONST_HOUSE_LIMIT

    def test_remove_hotel_empty(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = 0
        with pytest.raises(ValueError, match="No hotels to remove"):
            prop_space_monopoly.remove_hotel()

    def test_allow_remove_house(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = 1
        assert prop_space_monopoly.allow_remove_house() is True

    def test_allow_remove_house_empty(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_houses = 0
        assert prop_space_monopoly.allow_remove_house() is False

    def test_allow_remove_house_same_num(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        for property_ in prop_space_multi_monopoly.property_set.properties:
            assert isinstance(property_, space.PropertySpace)
            property_.no_of_houses = 1
        assert prop_space_multi_monopoly.allow_remove_house() is True

    def test_allow_remove_house_one_less_with_hotel(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_hotels = 1  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = prop_space_multi_monopoly.HOUSE_LIMIT
        assert prop_space_multi_monopoly.allow_remove_house() is False

    def test_allow_remove_house_one_less_without_hotel(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_houses = 3  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = 2
        assert prop_space_multi_monopoly.allow_remove_house() is False

    def test_allow_remove_house_one_more(
        self, prop_space_multi_monopoly: space.PropertySpace
    ):
        prop_space_multi_monopoly.property_set.properties[
            1
        ].no_of_houses = 2  # pyright: reportGeneralTypeIssues=false
        prop_space_multi_monopoly.no_of_houses = 3
        assert prop_space_multi_monopoly.allow_remove_house() is True

    def test_allow_remove_hotel(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = 1
        assert prop_space_monopoly.allow_remove_hotel() is True

    def test_allow_remove_hotel_empty(self, prop_space_monopoly: space.PropertySpace):
        prop_space_monopoly.no_of_hotels = 0
        assert prop_space_monopoly.allow_remove_hotel() is False


class TestTrigger:
    def test_trigger_unowned(
        self, prop_space_simple: space.PropertySpace, player_simple: player.Player
    ):
        assert prop_space_simple.trigger(player_simple) == Action.ASK_TO_BUY

    def test_trigger_diff_owner(
        self, prop_space_diff_owners: space.PropertySpace, player_simple: player.Player
    ):
        assert prop_space_diff_owners.trigger(player_simple) == Action.PAY_RENT

    def test_trigger_same_owner(
        self, prop_space_diff_owners: space.PropertySpace, player_simple: player.Player
    ):
        player_simple.uid = 1
        assert prop_space_diff_owners.trigger(player_simple) == Action.NOTHING
