# pyright: reportPrivateUsage=false
from typing import Callable, Iterable

import constants as c
import host
import pytest
from game import card, space
from game.actions import Action
from game.game import Game
from game.player import Player
from game.positions import Position


@pytest.fixture
def localhost_init(users_simple: list[host.User]) -> host.LocalHost:
    return host.LocalHost(users=users_simple)


@pytest.fixture
def localhost_begin(
    localhost_init: host.LocalHost, game_beginning: Game
) -> host.LocalHost:
    localhost_init.game = game_beginning
    return localhost_init


@pytest.fixture
def localhost_middle(
    localhost_begin: host.LocalHost, game_middle: Game
) -> host.LocalHost:
    localhost_begin.game = game_middle
    return localhost_begin


@pytest.fixture
def localhost_fake_player(
    localhost_begin: host.LocalHost, fake_player: Player
) -> host.LocalHost:
    localhost_begin.game.players[0] = fake_player
    return localhost_begin


@pytest.fixture
def chance_card() -> card.ChanceCard:
    return card.ChanceCard(
        id=9001, description="pytest", action=Action.NOTHING, ownable=False
    )


@pytest.fixture
def fake_player() -> Player:
    return Player(name="Fake Player", uid=0, cash=1500, position=0)


def patch_input(
    responses: Iterable[str] | str, monkeypatch: pytest.MonkeyPatch
) -> None:
    if isinstance(responses, str):
        responses = [responses]
    func: Callable[[str], str] = lambda prompt: next(iter(responses))
    monkeypatch.setattr("builtins.input", func)


class TestLocalhostInit:
    def test_localhost_init(self, localhost_init: host.LocalHost):
        assert isinstance(localhost_init.game, Game)
        assert len(localhost_init.user_to_player) == len(localhost_init.player_to_user)
        for player_uid, user_uid in localhost_init.player_to_user.items():
            assert player_uid == localhost_init.user_to_player[user_uid]

    def test_localhost_assign_token(
        self, localhost_init: host.LocalHost, users_simple: list[host.User]
    ):
        localhost_init.assign_player_token(users_simple[1], 5)
        player_uid = localhost_init.user_to_player[users_simple[1].uid]
        assert localhost_init.game.players[player_uid].token == 5


class TestSpaceTrigger:
    def test_space_trigger_to_buy_unowned(
        self,
        localhost_fake_player: host.LocalHost,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
    ):
        """Special cases such as not enough cash are tested in Game class"""
        fake_player.position = 8
        property_ = localhost_fake_player.game.game_map.map_list[8]
        assert isinstance(property_, space.Property)

        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.cash == 1500 - property_.price
        assert property_ in fake_player.properties

    def test_space_trigger_nothing(
        self, localhost_fake_player: host.LocalHost, fake_player: Player
    ):
        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.cash == 1500


class TestProcessChanceCard:
    @pytest.mark.parametrize(
        "action,position",
        [
            (Action.SEND_TO_BOARDWALK, Position.BOARDWALK),
            (Action.SEND_TO_ILLINOIS_AVE, Position.ILLINOIS_AVE),
            (Action.SEND_TO_ST_CHARLES_PLACE, Position.ST_CHARLES_PLACE),
            (Action.SEND_TO_READING_RAILROAD, Position.READING_RAILROAD),
        ],
    )
    def test_chance_send_to_property_buy(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
        action: Action,
        position: Position,
    ):
        chance_card.action = action
        property_ = localhost_fake_player.game.game_map.map_list[position.value]
        assert isinstance(property_, space.Property)
        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._process_chance_card(
                player_uid=0, drawn_card=chance_card
            )
        assert end_turn is False
        assert fake_player.position == position.value
        assert fake_player.cash == 1500 - property_.price
        assert property_ in fake_player.properties

    @pytest.mark.parametrize(
        "action,cur_pos,true_pos",
        [
            (
                Action.SEND_TO_NEAREST_RAILROAD,
                Position.RAILROADS.value[0] - 1,
                Position.RAILROADS.value[0],
            ),
            (
                Action.SEND_TO_NEAREST_RAILROAD,
                Position.RAILROADS.value[0] + 1,
                Position.RAILROADS.value[1],
            ),
            (
                Action.SEND_TO_NEAREST_RAILROAD,
                Position.RAILROADS.value[-1] - 1,
                Position.RAILROADS.value[-1],
            ),
            (
                Action.SEND_TO_NEAREST_RAILROAD,
                Position.RAILROADS.value[-1] + 1,
                Position.RAILROADS.value[0],
            ),
            (
                Action.SEND_TO_NEAREST_UTILITY,
                Position.UTILITIES.value[0] - 1,
                Position.UTILITIES.value[0],
            ),
            (
                Action.SEND_TO_NEAREST_UTILITY,
                Position.UTILITIES.value[0] + 1,
                Position.UTILITIES.value[1],
            ),
            (
                Action.SEND_TO_NEAREST_UTILITY,
                Position.UTILITIES.value[-1] - 1,
                Position.UTILITIES.value[-1],
            ),
            (
                Action.SEND_TO_NEAREST_UTILITY,
                Position.UTILITIES.value[-1] + 1,
                Position.UTILITIES.value[0],
            ),
        ],
    )
    def test_chance_send_to_nearest_xxx(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
        action: Action,
        cur_pos: int,
        true_pos: int,
    ):
        chance_card.action = action
        property_ = localhost_fake_player.game.game_map.map_list[true_pos]
        fake_player.position = cur_pos
        assert isinstance(property_, space.Property)

        go_offset = c.CONST_GO_CASH if cur_pos >= true_pos else 0
        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._process_chance_card(
                player_uid=0, drawn_card=chance_card
            )
        assert end_turn is False
        assert fake_player.position == true_pos
        assert fake_player.cash == 1500 - property_.price + go_offset
        assert property_ in fake_player.properties

    def test_chance_send_back_three_buy(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
    ):
        chance_card.action = Action.SEND_BACK_THREE_SPACES
        fake_player.position = 8 + 3
        property_ = localhost_fake_player.game.game_map.map_list[8]
        assert isinstance(property_, space.Property)
        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._process_chance_card(
                player_uid=0, drawn_card=chance_card
            )
        assert end_turn is False
        assert fake_player.position == 8
        assert fake_player.cash == 1500 - property_.price
        assert property_ in fake_player.properties

    def test_chance_send_to_go(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
    ):
        chance_card.action = Action.SEND_TO_GO

        end_turn = localhost_fake_player._process_chance_card(
            player_uid=0, drawn_card=chance_card
        )
        assert end_turn is False
        assert fake_player.position == Position.GO.value
        assert fake_player.cash == 1500 + c.CONST_GO_CASH

    def test_chance_send_to_jail(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
    ):
        chance_card.action = Action.SEND_TO_JAIL

        end_turn = localhost_fake_player._process_chance_card(
            player_uid=0, drawn_card=chance_card
        )
        assert end_turn is True
        assert fake_player.position == Position.JAIL.value
        assert fake_player.cash == 1500

    @pytest.mark.parametrize(
        "action,amount",
        [
            (Action.COLLECT_DIVIDEND, c.CONST_COLLECT_DIVIDEND),
            (Action.COLLECT_LOAN, c.CONST_COLLECT_LOAN),
            (Action.COLLECT_BANK_ERROR, c.CONST_COLLECT_BANK_ERROR),
            (Action.COLLECT_STOCK_SALE, c.CONST_COLLECT_STOCK_SALE),
            (Action.COLLECT_HOLIDAY_FUND, c.CONST_COLLECT_HOLIDAY_FUND),
            (Action.COLLECT_TAX_REFUND, c.CONST_COLLECT_TAX_REFUND),
            (Action.COLLECT_INSURANCE, c.CONST_COLLECT_INSURANCE),
            (Action.COLLECT_CONSULTANCY_FEE, c.CONST_COLLECT_CONSULTANCY_FEE),
            (Action.COLLECT_CONTEST_PRIZE, c.CONST_COLLECT_CONTEST_PRIZE),
            (Action.COLLECT_INHERITANCE, c.CONST_COLLECT_INHERITANCE),
            (Action.CHARGE_POOR_TAX, -c.CONST_POOR_TAX),
            (Action.CHARGE_DOCTOR_FEE, -c.CONST_DOCTOR_FEE),
            (Action.CHARGE_HOSPITAL_FEE, -c.CONST_HOSPITAL_FEE),
            (Action.CHARGE_SCHOOL_FEE, -c.CONST_SCHOOL_FEE),
        ],
    )
    def test_chance_collect_or_charge_cash(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
        action: Action,
        amount: int,
    ):
        chance_card.action = action

        end_turn = localhost_fake_player._process_chance_card(
            player_uid=0, drawn_card=chance_card
        )
        assert end_turn is False
        assert fake_player.cash == 1500 + amount

    @pytest.mark.parametrize(
        "action,amount",
        [
            (Action.COLLECT_GRAND_OPERA_NIGHT, c.CONST_GRAND_OPERA_NIGHT),
            (Action.COLLECT_BIRTHDAY, c.CONST_BIRTHDAY),
            (Action.PAY_CHAIRMAN_FEE, -c.CONST_CHAIRMAN_FEE),
        ],
    )
    def test_chance_collect_or_charge_players(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
        action: Action,
        amount: int,
    ):
        chance_card.action = action
        end_turn = localhost_fake_player._process_chance_card(
            player_uid=0, drawn_card=chance_card
        )

        for o_player in localhost_fake_player.game.players:
            if o_player.uid != fake_player.uid:
                assert o_player.cash == c.CONST_STARTING_CASH - amount
        amount = amount * (len(localhost_fake_player.game.players) - 1)

        assert end_turn is False
        assert fake_player.cash == 1500 + amount

    @pytest.mark.parametrize(
        "action,house_fee,hotel_fee",
        [
            (
                Action.CHARGE_GENERAL_REPAIR_FEE,
                c.CONST_GENERAL_REPAIR_HOUSE,
                c.CONST_GENERAL_REPAIR_HOTEL,
            ),
            (
                Action.CHARGE_STREET_REPAIR_FEE,
                c.CONST_STREET_REPAIR_HOUSE,
                c.CONST_STREET_REPAIR_HOTEL,
            ),
        ],
    )
    def test_chance_charge_repair(
        self,
        localhost_middle: host.LocalHost,
        chance_card: card.ChanceCard,
        action: Action,
        house_fee: int,
        hotel_fee: int,
    ):
        player = localhost_middle.game.players[1]
        old_cash = player.cash
        chance_card.action = action
        end_turn = localhost_middle._process_chance_card(
            player_uid=1, drawn_card=chance_card
        )

        assert end_turn is False
        assert player.cash == old_cash - house_fee * 4 - hotel_fee * 1
