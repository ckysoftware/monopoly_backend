import pytest
from src.game.actions import Action as a
from src.game.place.property_set import PropertySet
from src.game.place.utility_card import UtilityCard
from src.game.player import Player


@pytest.fixture
def util_card_simple():
    property_set = PropertySet(set_id=0)
    utility_card = UtilityCard(
        name="Utility 1",
        price=150,
        property_set=property_set,
    )
    property_set.add_property(utility_card)
    return utility_card


@pytest.fixture
def util_card_monopoly():
    property_set = PropertySet(set_id=0)
    utility_card = UtilityCard(
        name="Utility 1",
        price=150,
        property_set=property_set,
    )
    property_set.add_property(utility_card)
    property_set.monopoly = True
    return utility_card


@pytest.fixture
def util_card_diff_owners():
    property_set = PropertySet(set_id=0)
    util_card_1 = UtilityCard(
        name="Utility 1",
        price=150,
        property_set=property_set,
        owner_uid=1,
    )
    util_card_2 = UtilityCard(
        name="Utility 2",
        price=150,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(util_card_1)
    property_set.add_property(util_card_2)
    return util_card_1


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0)
    return player


def test_utility_card_init(util_card_simple):
    assert util_card_simple.name == "Utility 1"
    assert util_card_simple.price == 150
    assert util_card_simple.property_set.set_id == 0
    assert id(util_card_simple.property_set.properties[0]) == id(util_card_simple)
    assert util_card_simple.mortgaged is False
    assert util_card_simple.owner_uid is None


def test_assign_owner(util_card_simple):
    util_card_simple.assign_owner(2)
    assert util_card_simple.owner_uid == 2


def test_assign_owner_not_monopoly(util_card_diff_owners):
    util_card_diff_owners.assign_owner(2)
    assert util_card_diff_owners.property_set.monopoly is False


def test_assign_owner_is_monopoly(util_card_diff_owners):
    util_card_diff_owners.assign_owner(10)
    assert util_card_diff_owners.property_set.monopoly is True


def test_compute_rent_without_monopoly(util_card_simple):
    assert util_card_simple.compute_rent(dice_count=5) == 20


def test_compute_rent_with_monopoly(util_card_monopoly):
    assert util_card_monopoly.compute_rent(dice_count=10) == 100


def test_compute_rent_mortgaged_without_monopoly(util_card_simple):
    util_card_simple.mortgaged = True
    assert util_card_simple.compute_rent(dice_count=10) == 0


def test_compute_rent_mortgaged_with_monopoly(util_card_monopoly):
    util_card_monopoly.mortgaged = True
    assert util_card_monopoly.compute_rent(dice_count=5) == 0


def test_mortgage(util_card_diff_owners):
    util_card_diff_owners.mortgage()
    assert util_card_diff_owners.mortgaged is True


def test_mortgage_again(util_card_diff_owners):
    util_card_diff_owners.mortgage()
    with pytest.raises(ValueError, match="Property is already mortgaged"):
        util_card_diff_owners.mortgage()


def test_mortgage_no_owner(util_card_simple):
    with pytest.raises(ValueError, match="Property has no owner"):
        util_card_simple.mortgage()


def test_trigger_unowned(util_card_simple, player_simple):
    assert util_card_simple.trigger(player_simple) == a.ASK_TO_BUY


def test_trigger_diff_owner(util_card_diff_owners, player_simple):
    assert util_card_diff_owners.trigger(player_simple) == a.CHARGE_RENT


def test_trigger_same_owner(util_card_diff_owners, player_simple):
    player_simple.uid = 1
    assert util_card_diff_owners.trigger(player_simple) == a.NOTHING
