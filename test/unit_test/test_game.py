import constants as c
import pytest
from game.actions import Action
from game.game import Game
from game.game_map import GameMap
from game.player import Player
from game.space import PropertySet, PropertySpace


@pytest.fixture
def game_map_simple() -> GameMap:
    property_set = PropertySet(id=0)
    property_space_1 = PropertySpace(
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
    property_space_2 = PropertySpace(
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
    game_map = GameMap(map_list=[property_space_1, property_space_2])
    return game_map


@pytest.fixture
def game_init(game_map_simple: GameMap) -> Game:
    game = Game(game_map=game_map_simple)
    return game


@pytest.fixture
def game_with_players(game_init: Game) -> Game:
    for i in range(4):
        new_player = Player(name=f"Player {i + 1}", uid=i, cash=c.CONST_STARTING_CASH)
        game_init.players.append(new_player)
    return game_init


def test_game_init(game_init: Game, game_map_simple: GameMap):
    assert id(game_init.game_map) == id(game_map_simple)
    assert game_init.players == []
    assert game_init.current_player_uid is None
    assert game_init._roll_double_counter is None  # pyright: reportPrivateUsage=false


def test_game_add_player(game_with_players: Game):
    game_with_players.add_player(name="Testing Player")
    assert len(game_with_players.players) == 5

    player = game_with_players.players[-1]
    assert player.name == "Testing Player"
    assert player.uid == 4


def test_roll_dice(game_with_players: Game):
    for _ in range(100):
        dice_rolls = game_with_players.roll_dice()
        for roll in dice_rolls:
            assert roll in list(range(1, 7))


def test_move_player(game_with_players: Game):
    new_pos = game_with_players.move_player(player_uid=0, steps=8)
    assert new_pos == 8
    assert game_with_players.players[0].position == 8


def test_offset_go_pos(game_with_players: Game):
    new_pos = game_with_players.move_player(player_uid=0, steps=3)
    new_pos = game_with_players.offset_go_pos(player_uid=0)
    assert new_pos == 1
    assert game_with_players.players[0].position == 1


def test_initilize_first_player(game_with_players: Game):
    roll_result = game_with_players.initialize_first_player()

    recon_result: list[tuple[int, int]] = []  # reconstruct the orders
    for player_uid, dice_rolls in roll_result.items():
        recon_result.append((sum(dice_rolls), player_uid))

    recon_result.sort(
        key=lambda x: (x[0], -1 * x[1]), reverse=True
    )  # smaller uid first
    first_player = recon_result[0][1]
    assert first_player == game_with_players.current_player_uid


def test_check_double_roll_with_none(game_with_players: Game):
    action = game_with_players.check_double_roll(player_uid=2, dice_1=5, dice_2=5)
    assert action is Action.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 1)


def test_check_double_roll_with_one_count(game_with_players: Game):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=1)
    assert action is Action.ASK_TO_ROLL
    assert game_with_players._roll_double_counter == (2, 2)


def test_check_double_roll_over_limit(game_with_players: Game):
    game_with_players._roll_double_counter = (2, 2)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=3, dice_2=3)
    assert action is Action.SEND_TO_JAIL
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_not_double_reset(game_with_players: Game):
    game_with_players._roll_double_counter = (2, 1)
    action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=3)
    assert action is Action.NOTHING
    assert game_with_players._roll_double_counter is None


def test_check_double_roll_diff_player_incorrect_reset(game_with_players: Game):
    game_with_players._roll_double_counter = (2, 1)
    with pytest.raises(
        ValueError, match="Roll double counter has not been resetted correctly"
    ):
        _ = game_with_players.check_double_roll(player_uid=5, dice_1=1, dice_2=1)


def test_check_go_pass_false(game_with_players: Game):
    game_with_players.players[0].position = 1
    action = game_with_players.check_go_pass(player_uid=0)
    assert action == Action.NOTHING


def test_check_go_pass_true(game_with_players: Game):
    game_with_players.players[0].position = 3
    action = game_with_players.check_go_pass(player_uid=0)
    assert action == Action.PASS_GO


def test_trigger_space(game_with_players: Game):
    game_with_players.players[0].position = 1
    action = game_with_players.trigger_space(player_uid=0)
    assert action == Action.PAY_RENT


def test_add_player_cash(game_with_players: Game):
    new_cash = game_with_players.add_player_cash(player_uid=0, amount=300)
    assert new_cash == c.CONST_STARTING_CASH + 300
    assert game_with_players.players[0].cash == c.CONST_STARTING_CASH + 300


def test_sub_player_cash(game_with_players: Game):
    new_cash = game_with_players.sub_player_cash(player_uid=0, amount=600)
    assert new_cash == c.CONST_STARTING_CASH - 600
    assert game_with_players.players[0].cash == c.CONST_STARTING_CASH - 600


def test_next_player(game_with_players: Game):
    game_with_players.initialize_first_player()
    cur_player = game_with_players.current_player_uid
    next_player = game_with_players.next_player()
    assert cur_player is not None
    assert next_player == (cur_player + 1) % len(game_with_players.players)


def test_initialize_game_map(game_init: Game):
    game_init.initialize_game_map()
    map_names: list[str] = [
        "Go",
        "Mediterranean Avenue",
        "Community Chest",
        "Baltic Avenue",
        "Income Tax",
        "Reading Railroad",
        "Oriental Avenue",
        "Chance",
        "Vermont Avenue",
        "Connecticut Avenue",
        "Jail",
        "St. Charles Place",
        "Electric Company",
        "States Avenue",
        "Virginia Avenue",
        "Pennsylvania Railroad",
        "St. James Place",
        "Community Chest",
        "Tennessee Avenue",
        "New York Avenue",
        "Free Parking",
        "Kentucky Avenue",
        "Chance",
        "Indiana Avenue",
        "Illinois Avenue",
        "B. & O. Railroad",
        "Atlantic Avenue",
        "Ventnor Avenue",
        "Water Works",
        "Marvin Gardens",
        "Go To Jail",
        "Pacific Avenue",
        "North Carolina Avenue",
        "Community Chest",
        "Pennsylvania Avenue",
        "Short Line",
        "Chance",
        "Park Place",
        "Luxury Tax",
        "Boardwalk",
    ]
    assert game_init.game_map is not None
    assert len(game_init.game_map.map_list) == 40
    for i in range(len(map_names)):
        assert game_init.game_map.map_list[i].name == map_names[i]
