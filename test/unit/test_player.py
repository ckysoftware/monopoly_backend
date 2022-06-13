import constants as c
import pytest
from game import card, space
from game.player import Player


@pytest.fixture
def player_comp(prop_space_simple: space.PropertySpace):
    player = Player(
        name="Player 2",
        uid=1,
        token=3,
        properties=[prop_space_simple],
        cash=3000,
        position=10,
    )
    return player


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


def test_player_init(
    player_simple: Player, player_comp: Player, prop_space_simple: space.PropertySpace
):
    assert player_simple.name == "Player 1"
    assert player_simple.uid == 0
    assert player_simple.properties == []
    assert player_simple.cash == c.CONST_STARTING_CASH
    assert player_simple.position == 0
    assert len(player_simple.jail_cards) == 0

    assert player_comp.name == "Player 2"
    assert player_comp.uid == 1
    assert player_comp.token == 3
    assert player_comp.properties == [prop_space_simple]
    assert player_comp.cash == 3000
    assert player_comp.position == 10
    assert len(player_comp.jail_cards) == 0


def test_assign_token(player_simple: Player, player_comp: Player):
    player_simple.assign_token(5)
    player_comp.assign_token(10)
    assert player_simple.token == 5
    assert player_comp.token == 10


def test_add_property(player_simple: Player, prop_space_simple: space.PropertySpace):
    player_simple.add_property(prop_space_simple)
    assert len(player_simple.properties) == 1
    assert id(player_simple.properties[0]) == id(prop_space_simple)


def test_add_cash(player_comp: Player):
    new_balance = player_comp.add_cash(1000)
    assert new_balance == 4000
    assert player_comp.cash == 4000


def test_sub_cash(player_comp: Player):
    new_balance = player_comp.sub_cash(500)
    assert new_balance == 2500
    assert player_comp.cash == 2500


def test_move_player_from_zero(player_simple: Player):
    assert player_simple.move(steps=10) == 10
    assert player_simple.position == 10


def test_move_player_from_nonzero(player_comp: Player):
    assert player_comp.move(steps=10) == 20
    assert player_comp.position == 20


def test_move_player_by_position(player_comp: Player):
    assert player_comp.move(position=3) == 3
    assert player_comp.position == 3


def test_move_player_no_args(player_comp: Player):
    with pytest.raises(ValueError, match=("Either steps or position must be provided")):
        player_comp.move()


def test_move_player_positional_arg(player_comp: Player):
    assert player_comp.move(6) == 6
    assert player_comp.position == 6


def test_move_player_both_args(player_comp: Player):
    assert player_comp.move(8, 10) == 8
    assert player_comp.position == 8


def test_offset_position(player_comp: Player):
    pos = player_comp.move(steps=25)
    pos = player_comp.offset_position(10)
    assert pos == 25
    assert player_comp.position == 25


def test_add_jail_card(player_simple: Player, fake_jail_card: card.ChanceCard):
    player_simple.add_jail_card(fake_jail_card)
    assert player_simple.jail_cards[0] is fake_jail_card
    assert player_simple.get_jail_card_ids() == [1]


def test_use_jail_card(player_simple: Player, fake_jail_card: card.ChanceCard):
    player_simple.add_jail_card(fake_jail_card)
    assert player_simple.use_jail_card() is fake_jail_card
    assert len(player_simple.get_jail_card_ids()) == 0


def test_use_jail_card_no_card(player_simple: Player):
    with pytest.raises(ValueError, match="No jail cards available"):
        _ = player_simple.use_jail_card()
