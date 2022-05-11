import constants as c
import pytest
from game.actions import Action
from game.game import Game
from game.game_map import GameMap
from game.player import Player
from game.space import PropertySet, PropertySpace


@pytest.fixture
def game_init():
    property_set = PropertySet(set_id=0)
    property_space_1 = PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        CONST_HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        CONST_HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=1,
    )
    property_space_2 = PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        CONST_HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        CONST_HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    game_map = GameMap(map_list=[property_space_1, property_space_2])
    game = Game(game_map=game_map)
    return game, game_map


@pytest.fixture
def game_with_players():
    property_set = PropertySet(set_id=0)
    property_space_1 = PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        CONST_HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        CONST_HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=1,
    )
    property_space_2 = PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        CONST_HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        CONST_HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    game_map = GameMap(map_list=[property_space_1, property_space_2])
    game = Game(game_map=game_map)
    for i in range(4):
        new_player = Player(name=f"Player {i + 1}", uid=i, cash=c.CONST_STARTING_CASH)
        game.players.append(new_player)
    return game


def test_game_init(game_init):
    game, game_map = game_init
    assert id(game.game_map) == id(game_map)
    assert game.players == []
    assert game.current_player_uid is None
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
    new_pos = game_with_players.move_player(player_uid=0, steps=8)
    assert new_pos == 8
    assert game_with_players.players[0].position == 8


def test_offset_go_pos(game_with_players):
    new_pos = game_with_players.move_player(player_uid=0, steps=3)
    new_pos = game_with_players.offset_go_pos(player_uid=0)
    assert new_pos == 1
    assert game_with_players.players[0].position == 1


def test_initilize_first_player(game_with_players):
    roll_result = game_with_players.initilize_first_player()

    recon_result = []  # reconstruct the order from the roll result
    for player_uid, dice_rolls in roll_result.items():
        dice_1, dice_2 = dice_rolls
        recon_result.append((dice_1 + dice_2, player_uid))

    recon_result.sort(
        key=lambda x: (x[0], -1 * x[1]), reverse=True
    )  # smaller uid first
    first_player = recon_result[0][1]
    assert first_player == game_with_players.current_player_uid


def test_check_double_roll_with_none(game_with_players):
    action = game_with_players.check_double_roll(player_uid=2, dice_1=5, dice_2=5)
    assert action is Action.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 1)


def test_check_double_roll_with_one_count(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=1)
    assert action is Action.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 2)


def test_check_double_roll_over_limit(game_with_players):
    game_with_players._roll_double_counter = (2, 2)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=3, dice_2=3)
    assert action is Action.SEND_TO_JAIL
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_not_double_reset(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=3)
    assert action is Action.NOTHING
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_diff_player_incorrect_reset(game_with_players):
    game_with_players._roll_double_counter = (2, 1)
    with pytest.raises(
        ValueError, match="Roll double counter has not been resetted correctly"
    ):
        _ = game_with_players.check_double_roll(player_uid=5, dice_1=1, dice_2=1)


def test_check_go_pass_false(game_with_players):
    game_with_players.players[0].position = 1
    action = game_with_players.check_go_pass(player_uid=0)
    assert action == Action.NOTHING


def test_check_go_pass_true(game_with_players):
    game_with_players.players[0].position = 3
    action = game_with_players.check_go_pass(player_uid=0)
    assert action == Action.PASS_GO


def test_trigger_space(game_with_players):
    game_with_players.players[0].position = 1
    action = game_with_players.trigger_space(player_uid=0)
    assert action == Action.PAY_RENT


def test_add_player_cash(game_with_players):
    new_cash = game_with_players.add_player_cash(player_uid=0, amount=300)
    assert new_cash == c.CONST_STARTING_CASH + 300
    assert game_with_players.players[0].cash.balance == c.CONST_STARTING_CASH + 300


def test_sub_player_cash(game_with_players):
    new_cash = game_with_players.sub_player_cash(player_uid=0, amount=600)
    assert new_cash == c.CONST_STARTING_CASH - 600
    assert game_with_players.players[0].cash.balance == c.CONST_STARTING_CASH - 600
