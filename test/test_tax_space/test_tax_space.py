import constants as c
import pytest
from game import enum_types, player, space
from game.actions import Action


@pytest.fixture
def player_simple():
    player_simple = player.Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player_simple


@pytest.fixture
def tax_space_income_tax():
    tax_space_income = space.TaxSpace(
        name="Income Tax", tax_type=enum_types.TaxType.INCOME
    )
    return tax_space_income


@pytest.fixture
def tax_space_luxury_tax():
    tax_space_luxuary = space.TaxSpace(
        name="Luxury Tax", tax_type=enum_types.TaxType.LUXURY
    )
    return tax_space_luxuary


def test_tax_space_income_init(tax_space_income_tax):
    assert tax_space_income_tax.name == "Income Tax"
    assert tax_space_income_tax.tax_type == enum_types.TaxType.INCOME


def test_tax_space_luxury_init(tax_space_luxury_tax):
    assert tax_space_luxury_tax.name == "Luxury Tax"
    assert tax_space_luxury_tax.tax_type == enum_types.TaxType.LUXURY


def test_tax_space_income_trigger(tax_space_income_tax, player_simple):
    assert (
        tax_space_income_tax.trigger(player=player_simple) == Action.CHARGE_INCOME_TAX
    )


def test_tax_space_luxury_trigger(tax_space_luxury_tax, player_simple):
    assert (
        tax_space_luxury_tax.trigger(player=player_simple) == Action.CHARGE_LUXURY_TAX
    )


def test_tax_space_unknown_init():
    with pytest.raises(ValueError, match="Unknown tax type."):
        unknown = space.TaxSpace(name="Unknown", tax_type="unknown")  # noqa: F841
