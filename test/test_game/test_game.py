import pytest
import src.constants as c
from src.game.actions import Action as A
from src.game.game import Game
from src.game.game_map import GameMap
from src.game.place.property.property_card import PropertyCard
from src.game.place.property.property_set import PropertySet
from src.game.player import Player


@pytest.fixture
def game_init():
    property_set = PropertySet(set_id=0)
    property_card_1 = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=1,
    )
    property_card_2 = PropertyCard(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_card_1)
    property_set.add_property(property_card_2)
    game_map = GameMap(map_list=[property_card_1, property_card_2])
    game = Game(game_map=game_map)
    return game, game_map


@pytest.fixture
def game_with_players():
    property_set = PropertySet(set_id=0)
    property_card_1 = PropertyCard(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=1,
    )
    property_card_2 = PropertyCard(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_card_1)
    property_set.add_property(property_card_2)
    game_map = GameMap(map_list=[property_card_1, property_card_2])
    game = Game(game_map=game_map)
    for i in range(4):
        new_player = Player(name=f"Player {i + 1}", uid=i)
        game.players.append(new_player)
    return game


def test_game_init(game_init):
    game, game_map = game_init
    assert id(game.game_map) == id(game_map)
    assert game.players == []
    assert game.current_order_pos is None
    assert game.player_order == []
    assert game._roll_double_counter is None


def test_game_add_player(game_with_players):
    game_with_players.add_player(name="Testing Player")
    assert len(game_with_players.players) == 5

    player = game_with_players.players[-1]
    assert player.name == "Testing Player"
    assert player.uid == 4


def test_roll_dice(game_with_players):
    for _ in range(100):
        dice_1, dice_2 = game_with_players.roll_dice()
        assert dice_1 in list(range(1, 7))
        assert dice_2 in list(range(1, 7))


def test_move_player(game_with_players):
    new_pos = game_with_players.move_player(uid=0, steps=8)
    assert new_pos == 8
    assert game_with_players.players[0].position == 8


def test_offset_go_pos(game_with_players):
    new_pos = game_with_players.move_player(uid=0, steps=3)
    new_pos = game_with_players.offset_go_pos(uid=0)
    assert new_pos == 1
    assert game_with_players.players[0].position == 1


def test_initilize_player_order(game_with_players):
    roll_result = game_with_players.initilize_player_order()
    recon_result = []  # reconstruct the order from the roll result
    for uid, dice_rolls in roll_result.items():
        dice_1, dice_2 = dice_rolls
        recon_result.append((dice_1 + dice_2, uid))
    recon_result.sort()
    recon_order = [x[1] for x in recon_result]

    assert recon_order == game_with_players.player_order
    assert len(roll_result) == len(game_with_players.player_order)

    player_order = (
        game_with_players.player_order.copy()
    )  # check all players are covered
    for uid in roll_result.keys():
        player_order.remove(uid)
    assert len(player_order) == 0


def test_check_double_roll_with_none(game_with_players):
    action = game_with_players.check_double_roll(uid=2, dice_1=5, dice_2=5)
    assert action is A.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 1)


def test_check_double_roll_with_one_count(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(uid=2, dice_1=1, dice_2=1)
    assert action is A.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 2)


def test_check_double_roll_over_limit(game_with_players):
    game_with_players._roll_double_counter = (2, 2)
    action = game_with_players.check_double_roll(uid=2, dice_1=3, dice_2=3)
    assert action is A.SEND_TO_JAIL
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_not_double_reset(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(uid=2, dice_1=1, dice_2=3)
    assert action is A.NOTHING
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_diff_player_incorrect_reset(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    with pytest.raises(
        ValueError, match="Roll double counter has not been resetted correctly"
    ):
        _ = game_with_players.check_double_roll(uid=5, dice_1=1, dice_2=1)


def test_check_go_pass_false(game_with_players):
    game_with_players.players[0].position = 1
    action = game_with_players.check_go_pass(uid=0)
    assert action == A.NOTHING


def test_check_go_pass_true(game_with_players):
    game_with_players.players[0].position = 3
    action = game_with_players.check_go_pass(uid=0)
    assert action == A.PASS_GO


def test_trigger_place(game_with_players):
    game_with_players.players[0].position = 1
    action = game_with_players.trigger_place(uid=0)
    assert action == A.CHARGE_RENT


def test_add_player_cash(game_with_players):
    new_cash = game_with_players.add_player_cash(uid=0, amount=300)
    assert new_cash == c.CONST_STARTING_CASH + 300
    assert game_with_players.players[0].cash.balance == c.CONST_STARTING_CASH + 300


def test_sub_player_cash(game_with_players):
    new_cash = game_with_players.sub_player_cash(uid=0, amount=600)
    assert new_cash == c.CONST_STARTING_CASH - 600
    assert game_with_players.players[0].cash.balance == c.CONST_STARTING_CASH - 600
