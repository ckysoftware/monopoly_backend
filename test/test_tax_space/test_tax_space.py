import constants as c
import pytest
from src.game.actions import Action as A
from src.game.player import Player
from src.game.space import TaxSpace


@pytest.fixture
def player_simple():
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


@pytest.fixture
def tax_space_income_tax():
    tax_space_income = TaxSpace(name="Income Tax", TAX_ACTION=A.CHARGE_INCOME_TAX)
    return tax_space_income


@pytest.fixture
def tax_space_luxary_tax():
    tax_space_luxuary = TaxSpace(name="Luxary Tax", TAX_ACTION=A.CHARGE_LUXARY_TAX)
    return tax_space_luxuary


def test_tax_space_income_init(tax_space_income_tax):
    assert tax_space_income_tax.name == "Income Tax"
    assert tax_space_income_tax.TAX_ACTION == A.CHARGE_INCOME_TAX


def test_tax_space_luxary_init(tax_space_luxary_tax):
    assert tax_space_luxary_tax.name == "Luxary Tax"
    assert tax_space_luxary_tax.TAX_ACTION == A.CHARGE_LUXARY_TAX


def test_tax_space_income_trigger(tax_space_income_tax, player_simple):
    assert tax_space_income_tax.trigger(player_simple) == A.CHARGE_INCOME_TAX


def test_tax_space_luxary_trigger(tax_space_luxary_tax, player_simple):
    assert tax_space_luxary_tax.trigger(player_simple) == A.CHARGE_LUXARY_TAX


def test_tax_space_income_init_other_tax_action():
    with pytest.raises(
        ValueError,
        match="Tax space must have a TAX_ACTION of either CHARGE_INCOME_TAX or CHARGE_LUXARY_TAX",
    ):
        TaxSpace(name="Income Tax", TAX_ACTION=A.NOTHING)
