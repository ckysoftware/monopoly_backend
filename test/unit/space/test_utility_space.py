import pytest

from game import player, space
from game.actions import Action


@pytest.fixture
def util_space_simple():
    property_set = space.PropertySet(id=0)
    utility_space = space.UtilitySpace(
        id=1,
        name="Utility 1",
        price=150,
        property_set=property_set,
    )
    property_set.add_property(utility_space)
    return utility_space


@pytest.fixture
def util_space_monopoly(util_space_simple: space.UtilitySpace):
    util_space_simple.property_set.monopoly = True
    return util_space_simple


@pytest.fixture
def util_space_diff_owners():
    property_set = space.PropertySet(id=0)
    util_space_1 = space.UtilitySpace(
        id=1,
        name="Utility 1",
        price=150,
        property_set=property_set,
        owner_uid=1,
    )
    util_space_2 = space.UtilitySpace(
        id=2,
        name="Utility 2",
        price=150,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(util_space_1)
    property_set.add_property(util_space_2)
    return util_space_1


def test_utility_space_init(util_space_simple: space.UtilitySpace):
    assert util_space_simple.name == "Utility 1"
    assert util_space_simple.price == 150
    assert util_space_simple.property_set.id == 0
    assert id(util_space_simple.property_set.properties[0]) == id(util_space_simple)
    assert util_space_simple.mortgaged is False
    assert util_space_simple.owner_uid is None


def test_assign_owner(util_space_simple: space.UtilitySpace):
    util_space_simple.assign_owner(2)
    assert util_space_simple.owner_uid == 2


def test_assign_owner_not_monopoly(util_space_diff_owners: space.UtilitySpace):
    util_space_diff_owners.assign_owner(2)
    assert util_space_diff_owners.property_set.monopoly is False


def test_assign_owner_is_monopoly(util_space_diff_owners: space.UtilitySpace):
    util_space_diff_owners.assign_owner(10)
    assert util_space_diff_owners.property_set.monopoly is True


def test_compute_rent_without_monopoly(util_space_simple: space.UtilitySpace):
    assert util_space_simple.compute_rent(dice_count=5) == 20


def test_compute_rent_with_monopoly(util_space_monopoly: space.UtilitySpace):
    assert util_space_monopoly.compute_rent(dice_count=10) == 100


def test_compute_rent_mortgaged_without_monopoly(util_space_simple: space.UtilitySpace):
    util_space_simple.mortgaged = True
    assert util_space_simple.compute_rent(dice_count=10) == 0


def test_compute_rent_mortgaged_with_monopoly(util_space_monopoly: space.UtilitySpace):
    util_space_monopoly.mortgaged = True
    assert util_space_monopoly.compute_rent(dice_count=5) == 0


def test_compute_rent_nonpositive_dice_count(util_space_simple: space.UtilitySpace):
    with pytest.raises(ValueError, match="Dice count must be positive"):
        util_space_simple.compute_rent()


class TestMortgage:
    def test_mortgage(self, util_space_diff_owners: space.UtilitySpace):
        util_space_diff_owners.mortgage()
        assert util_space_diff_owners.mortgaged is True

    def test_mortgage_again(self, util_space_diff_owners: space.UtilitySpace):
        util_space_diff_owners.mortgage()
        with pytest.raises(ValueError, match="Property is already mortgaged"):
            util_space_diff_owners.mortgage()

    def test_mortgage_no_owner(self, util_space_simple: space.UtilitySpace):
        with pytest.raises(ValueError, match="Property has no owner"):
            util_space_simple.mortgage()

    def test_allow_mortgage(self, util_space_diff_owners: space.UtilitySpace):
        assert util_space_diff_owners.allow_mortgage() is True

    def test_allow_mortgage_again(self, util_space_diff_owners: space.UtilitySpace):
        util_space_diff_owners.mortgage()
        assert util_space_diff_owners.allow_mortgage() is False

    def test_allow_mortgage_no_owner(self, util_space_simple: space.UtilitySpace):
        assert util_space_simple.allow_mortgage() is False


def test_trigger_unowned(
    util_space_simple: space.UtilitySpace, player_simple: player.Player
):
    assert util_space_simple.trigger(player_simple) == Action.ASK_TO_BUY


def test_trigger_diff_owner(
    util_space_diff_owners: space.UtilitySpace, player_simple: player.Player
):
    assert util_space_diff_owners.trigger(player_simple) == Action.PAY_RENT


def test_trigger_same_owner(
    util_space_diff_owners: space.UtilitySpace, player_simple: player.Player
):
    player_simple.uid = 1
    assert util_space_diff_owners.trigger(player_simple) == Action.NOTHING
