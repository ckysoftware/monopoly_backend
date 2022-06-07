import constants as c
import pytest
from game import card, space
from game.actions import Action
from game.game import Game
from game.game_map import GameMap


def fn_test_initialize_deck(
    game: Game, cc_card_list: set[int], chance_card_list: set[int]
):
    assert len(chance_card_list) == len(game.chance_deck.cards)
    assert len(cc_card_list) == len(game.cc_deck.cards)
    for chance_card in game.chance_deck.cards:
        assert chance_card.id in chance_card_list
    for cc_card in game.cc_deck.cards:
        assert cc_card.id in cc_card_list


def fn_test_initialize_game_map(game: Game, map_list: list[str]):
    assert game.game_map is not None
    assert len(game.game_map.map_list) == 40
    for i in range(len(map_list)):
        assert game.game_map.map_list[i].name == map_list[i]


class TestGameInitialization:
    def test_game_init(self, game_init: Game, game_map_simple: GameMap):
        assert id(game_init.game_map) == id(game_map_simple)
        assert game_init.players == []
        assert (
            game_init._roll_double_counter is None
        )  # pyright: reportPrivateUsage=false

    def test_game_add_player(self, game_with_players: Game):
        game_with_players.add_player(name="Testing Player")
        assert len(game_with_players.players) == 5

        player = game_with_players.players[-1]
        assert player.name == "Testing Player"
        assert player.uid == 4

    # NOTE try not to test non public method
    # def test_initialize_game_map(self, game_init: Game, map_list: list[str]):
    #     game_init._initialize_game_map()
    #     fn_test_initialize_game_map(game_init, map_list)

    # NOTE try not to test non public method
    # def test_initialize_deck(
    #     self, game_init: Game, chance_card_list: set[int], cc_card_list: set[int]
    # ):
    #     game_init._initialize_deck()
    #     fn_test_initialize_deck(game_init, cc_card_list, chance_card_list)

    def test_initialize(
        self,
        game_init: Game,
        map_list: list[str],
        cc_card_list: set[int],
        chance_card_list: set[int],
    ):
        game_init.initialize()
        fn_test_initialize_game_map(game_init, map_list)
        fn_test_initialize_deck(game_init, cc_card_list, chance_card_list)

    def test_initialize_first_player(self, game_with_players: Game):
        roll_result = game_with_players.initialize_first_player()

        recon_result: list[tuple[int, int]] = []  # reconstruct the orders
        for player_uid, dice_rolls in roll_result.items():
            recon_result.append((sum(dice_rolls), player_uid))

        recon_result.sort(
            key=lambda x: (x[0], -1 * x[1]), reverse=True
        )  # smaller uid first
        first_player = recon_result[0][1]
        assert first_player == game_with_players.current_player_uid


class TestMovePlayer:
    def test_move_player_by_steps(self, game_with_players: Game):
        new_pos = game_with_players.move_player(player_uid=0, steps=8)
        assert new_pos == 8
        assert game_with_players.players[0].position == 8

    def test_move_player_by_position(self, game_with_players: Game):
        new_pos = game_with_players.move_player(player_uid=0, position=15)
        assert new_pos == 15
        assert game_with_players.players[0].position == 15

    def test_move_player_no_args(self, game_with_players: Game):
        with pytest.raises(
            ValueError, match=("Either steps or position must be provided")
        ):
            _ = game_with_players.move_player(player_uid=0)

    def test_move_player_both_args(self, game_with_players: Game):
        new_pos = game_with_players.move_player(0, 20, 1)
        assert new_pos == 1
        assert game_with_players.players[0].position == 1

    def test_offset_go_pos(self, game_with_players: Game):
        new_pos = game_with_players.move_player(player_uid=0, steps=3)
        new_pos = game_with_players.offset_go_pos(player_uid=0)
        assert new_pos == 1
        assert game_with_players.players[0].position == 1


class TestRoll:
    def test_roll_dice(self, game_with_players: Game):
        for _ in range(100):
            dice_rolls = game_with_players.roll_dice()
            for roll in dice_rolls:
                assert roll in list(range(1, 7))

    def test_check_double_roll_with_none(self, game_with_players: Game):
        action = game_with_players.check_double_roll(player_uid=2, dice_1=5, dice_2=5)
        assert action is Action.ASK_TO_ROLL
        assert game_with_players._roll_double_counter == (2, 1)

    def test_check_double_roll_with_one_count(self, game_with_players: Game):
        game_with_players._roll_double_counter = (2, 1)
        action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=1)
        assert action is Action.ASK_TO_ROLL
        assert game_with_players._roll_double_counter == (2, 2)

    def test_check_double_roll_over_limit(self, game_with_players: Game):
        game_with_players._roll_double_counter = (2, 2)
        action = game_with_players.check_double_roll(player_uid=2, dice_1=3, dice_2=3)
        assert action is Action.SEND_TO_JAIL
        assert game_with_players._roll_double_counter is None

    def test_check_double_roll_not_double_reset(self, game_with_players: Game):
        game_with_players._roll_double_counter = (2, 1)
        action = game_with_players.check_double_roll(player_uid=2, dice_1=1, dice_2=3)
        assert action is Action.NOTHING
        assert game_with_players._roll_double_counter is None

    def test_check_double_roll_diff_player_incorrect_reset(
        self, game_with_players: Game
    ):
        game_with_players._roll_double_counter = (2, 1)
        with pytest.raises(
            ValueError, match="Roll double counter has not been resetted correctly"
        ):
            _action = game_with_players.check_double_roll(
                player_uid=5, dice_1=1, dice_2=1
            )


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


class TestDrawCard:
    def test_draw_chance_card_once(self, game_beginning: Game):
        drawn_card = game_beginning.draw_chance_card()
        assert isinstance(drawn_card, card.ChanceCard)
        assert isinstance(drawn_card.trigger(), Action)

    def test_draw_cc_card_once(self, game_beginning: Game):
        drawn_card = game_beginning.draw_cc_card()
        assert isinstance(drawn_card, card.ChanceCard)
        assert isinstance(drawn_card.trigger(), Action)

    def test_exhaust_chance_deck(self, game_beginning: Game):
        length = len(game_beginning.chance_deck.cards)
        drawn_cards: list[card.ChanceCard] = []
        length_after_exhaustion = length
        for _ in range(length):
            drawn_card = game_beginning.draw_chance_card()
            if drawn_card.trigger() != Action.COLLECT_JAIL_CARD:
                drawn_cards.append(drawn_card)
            else:
                length_after_exhaustion -= 1
        assert length_after_exhaustion == len(game_beginning.chance_deck.cards)
        for drawn_card in drawn_cards:
            assert drawn_card == game_beginning.draw_chance_card()

    def test_exhaust_cc_deck(self, game_beginning: Game):
        length = len(game_beginning.cc_deck.cards)
        drawn_cards: list[card.ChanceCard] = []
        length_after_exhaustion = length
        for _ in range(length):
            drawn_card = game_beginning.draw_cc_card()
            if drawn_card.trigger() != Action.COLLECT_JAIL_CARD:
                drawn_cards.append(drawn_card)
            else:
                length_after_exhaustion -= 1
        assert length_after_exhaustion == len(game_beginning.cc_deck.cards)
        for drawn_card in drawn_cards:
            assert drawn_card == game_beginning.draw_cc_card()


class TestGetInfo:
    def test_get_current_player(self, game_with_players: Game):
        game_with_players.current_player_uid = 1
        assert game_with_players.get_current_player() == ("Player 2", 1)

    def test_get_player_position(self, game_with_players: Game):
        game_with_players.players[1].position = 10
        assert game_with_players.get_player_position(player_uid=1) == 10

    def test_get_house_and_hotel_counts(self, game_middle: Game):
        house_count, hotel_count = game_middle.get_player_house_and_hotel_counts(1)
        assert house_count == 4
        assert hotel_count == 1

    def test_get_property_by_position(self, game_middle: Game):
        assert game_middle.get_property(1) == game_middle.game_map.map_list[1]

    def test_get_property_by_player_uid(self, game_middle: Game):
        game_middle.players[1].position = 5
        assert (
            game_middle.get_property(player_uid=1) == game_middle.game_map.map_list[5]
        )

    def test_get_property_both_args(self, game_middle: Game):
        game_middle.players[1].position = 5
        assert game_middle.get_property(8, 1) == game_middle.game_map.map_list[8]

    def test_get_property_no_args(self, game_middle: Game):
        with pytest.raises(
            ValueError, match="Either position or player_uid must be provided"
        ):
            _ = game_middle.get_property()

    def test_get_property_not_property(self, game_middle: Game):
        with pytest.raises(ValueError, match=r"Space is not a Property: .*"):
            _ = game_middle.get_property(position=4)


def test_next_player(game_with_players: Game):
    game_with_players.initialize_first_player()
    cur_player = game_with_players.current_player_uid
    next_player = game_with_players.next_player_and_reset()
    assert cur_player is not None
    assert next_player == (cur_player + 1) % len(game_with_players.players)


class TestAssignToken:
    def test_assign_player_token(self, game_with_players: Game):
        game_with_players.assign_player_token(player_uid=2, token=1)
        assert game_with_players.players[2].token == 1

    def test_assign_player_token_duplicated(self, game_with_players: Game):
        game_with_players.assign_player_token(player_uid=2, token=1)
        with pytest.raises(ValueError, match="Token is already assigned"):
            game_with_players.assign_player_token(player_uid=0, token=1)


class TestPropertyTransactions:
    def test_buy_property_with_position(self, game_middle: Game):
        ori_cash = game_middle.players[2].cash
        position = 8
        property_ = game_middle.game_map.map_list[position]
        assert isinstance(property_, space.Property)

        new_cash = game_middle.buy_property(player_uid=2, position=position)
        assert new_cash == ori_cash - property_.price
        assert game_middle.players[2].cash == new_cash
        assert property_ in game_middle.players[2].properties

    def test_buy_property_without_position(self, game_middle: Game):
        ori_cash = game_middle.players[2].cash
        position = 8
        game_middle.players[2].position = position
        property_ = game_middle.game_map.map_list[position]
        assert isinstance(property_, space.Property)

        new_cash = game_middle.buy_property(player_uid=2)
        assert new_cash == ori_cash - property_.price
        assert game_middle.players[2].cash == new_cash
        assert property_ in game_middle.players[2].properties

    def test_buy_property_not_property(self, game_middle: Game):
        with pytest.raises(ValueError, match=r"Space is not a Property: .*"):
            game_middle.buy_property(player_uid=2, position=4)

    def test_buy_property_owned(self, game_middle: Game):
        with pytest.raises(ValueError, match="Property is already owned"):
            game_middle.buy_property(player_uid=0, position=3)

    def test_buy_property_no_cash(self, game_middle: Game):
        game_middle.players[0].cash = 10
        with pytest.raises(ValueError, match=r"Player .* does not have enough cash$"):
            game_middle.buy_property(player_uid=0, position=8)

    def test_buy_property_transaction_without_price(self, game_middle: Game):
        property_ = game_middle.game_map.map_list[8]
        assert isinstance(property_, space.Property)
        player_ = game_middle.players[0]

        ori_cash = player_.cash
        new_cash = game_middle.buy_property_transaction(player_, property_)

        assert new_cash == player_.cash
        assert new_cash == ori_cash - property_.price
        assert property_.owner_uid == player_.uid
        assert property_ in player_.properties

    def test_buy_property_transaction_with_price(self, game_middle: Game):
        property_ = game_middle.game_map.map_list[8]
        assert isinstance(property_, space.Property)
        player_ = game_middle.players[0]
        price = 10

        ori_cash = player_.cash
        new_cash = game_middle.buy_property_transaction(player_, property_, price=price)

        assert new_cash == player_.cash
        assert new_cash == ori_cash - price
        assert property_.owner_uid == player_.uid
        assert property_ in player_.properties

    def test_auction_property(self, game_middle: Game):
        bidders = game_middle.auction_property(8)
        assert bidders == game_middle.players

    def test_auction_property_not_property(self, game_middle: Game):
        with pytest.raises(ValueError, match=r"Space is not a Property: .*"):
            _ = game_middle.auction_property(0)

    def test_auction_property_owned(self, game_middle: Game):
        with pytest.raises(ValueError, match="Property is already owned"):
            _ = game_middle.auction_property(3)
