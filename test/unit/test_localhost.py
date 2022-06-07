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

CHANCE_CARD_SPACE_POS = [7, 22, 36]


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
    """monkey patch the bultin input() with responses as input"""
    if isinstance(responses, str):
        responses = [responses]
    func: Callable[[str], str] = lambda _prompt: next(iter(responses))
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

    def test_space_trigger_send_to_jail(
        self, localhost_fake_player: host.LocalHost, fake_player: Player
    ):
        fake_player.position = 30
        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is True
        assert fake_player.cash == 1500

    def test_space_trigger_charge_income_tax(
        self, localhost_fake_player: host.LocalHost, fake_player: Player
    ):
        fake_player.position = 4
        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.cash == 1500 - c.CONST_INCOME_TAX

    def test_space_trigger_charge_luxury_tax(
        self, localhost_fake_player: host.LocalHost, fake_player: Player
    ):
        fake_player.position = 38
        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.cash == 1500 - c.CONST_LUXURY_TAX


@pytest.mark.parametrize("chance_pos", [7, 22, 36])
class TestSpaceTriggerDrawChanceCard:
    """Only positions of the chance card are tested because cc cards don't depend on positions"""

    def set_up(
        self,
        fake_player: Player,
        chance_pos: int,
        chance_card: card.ChanceCard,
        action: Action,
        monkeypatch: pytest.MonkeyPatch,
    ):
        """change player position to chance pos, monkey patch the drawn card to specific action"""
        chance_card.action = action
        fake_player.position = chance_pos
        func: Callable[[Game], card.ChanceCard] = lambda _: chance_card
        monkeypatch.setattr(Game, "draw_chance_card", func)

    @pytest.mark.parametrize(
        "action, position",
        [
            (Action.SEND_TO_BOARDWALK, Position.BOARDWALK),
            (Action.SEND_TO_BOARDWALK, Position.BOARDWALK),
            (Action.SEND_TO_BOARDWALK, Position.BOARDWALK),
            (Action.SEND_TO_ILLINOIS_AVE, Position.ILLINOIS_AVE),
            (Action.SEND_TO_ILLINOIS_AVE, Position.ILLINOIS_AVE),
            (Action.SEND_TO_ILLINOIS_AVE, Position.ILLINOIS_AVE),
            (Action.SEND_TO_ST_CHARLES_PLACE, Position.ST_CHARLES_PLACE),
            (Action.SEND_TO_ST_CHARLES_PLACE, Position.ST_CHARLES_PLACE),
            (Action.SEND_TO_ST_CHARLES_PLACE, Position.ST_CHARLES_PLACE),
            (Action.SEND_TO_READING_RAILROAD, Position.READING_RAILROAD),
            (Action.SEND_TO_READING_RAILROAD, Position.READING_RAILROAD),
            (Action.SEND_TO_READING_RAILROAD, Position.READING_RAILROAD),
        ],
    )
    def test_chance_card_send_to_property_buy(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
        chance_pos: int,
        action: Action,
        position: Position,
    ):
        self.set_up(fake_player, chance_pos, chance_card, action, monkeypatch)

        go_cash_offset = 200 if chance_pos >= position.value else 0
        property_ = localhost_fake_player.game.game_map.map_list[position.value]
        assert isinstance(property_, space.Property)
        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.position == position.value
        assert fake_player.cash == 1500 - property_.price + go_cash_offset
        assert property_ in fake_player.properties

    @pytest.mark.parametrize(
        "action",
        [Action.SEND_TO_NEAREST_RAILROAD, Action.SEND_TO_NEAREST_UTILITY],
    )
    def test_chance_card_send_to_nearest_xxx(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
        action: Action,
        chance_pos: int,
    ):
        self.set_up(fake_player, chance_pos, chance_card, action, monkeypatch)

        # test different chance space positions
        match chance_pos, action:
            case 7, Action.SEND_TO_NEAREST_RAILROAD:
                true_pos = Position.RAILROADS.value[1]
            case 7, Action.SEND_TO_NEAREST_UTILITY:
                true_pos = Position.UTILITIES.value[0]
            case 22, Action.SEND_TO_NEAREST_RAILROAD:
                true_pos = Position.RAILROADS.value[2]
            case 22, Action.SEND_TO_NEAREST_UTILITY:
                true_pos = Position.UTILITIES.value[1]
            case 36, Action.SEND_TO_NEAREST_RAILROAD:
                true_pos = Position.RAILROADS.value[0]
            case 36, Action.SEND_TO_NEAREST_UTILITY:
                true_pos = Position.UTILITIES.value[0]
            case _:
                raise ValueError("Unknown parameter for chance space position")

        property_ = localhost_fake_player.game.game_map.map_list[true_pos]
        assert isinstance(property_, space.Property)

        go_cash_offset = c.CONST_GO_CASH if chance_pos >= true_pos else 0
        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.position == true_pos
        assert fake_player.cash == 1500 - property_.price + go_cash_offset
        assert property_ in fake_player.properties

    def test_chance_card_send_back_three(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        monkeypatch: pytest.MonkeyPatch,
        fake_player: Player,
        chance_pos: int,
    ):
        self.set_up(
            fake_player,
            chance_pos,
            chance_card,
            Action.SEND_BACK_THREE_SPACES,
            monkeypatch,
        )

        # check different chance pos
        match chance_pos:
            case 7:  # income tax
                change_cash = -c.CONST_GO_CASH
            case 22:  # buy New York Avenue
                change_cash = -200
            case 36:  # draw cc card and pay $50
                change_cash = -50
            case _:
                raise ValueError("Unknown parameter for chance space position")

        # For the case where sending back 3 spaces will trigger cc card draw
        patched_cc_card: Callable[[Game], card.ChanceCard] = lambda _: card.ChanceCard(
            id=-1,
            description="pytest_cc_card",
            action=Action.CHARGE_DOCTOR_FEE,
            ownable=False,
        )
        monkeypatch.setattr(Game, "draw_cc_card", patched_cc_card)

        property_ = localhost_fake_player.game.game_map.map_list[chance_pos - 3]

        with monkeypatch.context() as m:
            patch_input("buy", m)
            end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)

        assert end_turn is False
        assert fake_player.position == chance_pos - 3
        assert fake_player.cash == 1500 + change_cash
        if isinstance(property_, space.Property):
            assert property_ in fake_player.properties

    def test_chance_card_send_to_go(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
        monkeypatch: pytest.MonkeyPatch,
        chance_pos: int,
    ):
        self.set_up(
            fake_player, chance_pos, chance_card, Action.SEND_TO_GO, monkeypatch
        )

        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
        assert end_turn is False
        assert fake_player.position == Position.GO.value
        assert fake_player.cash == 1500 + c.CONST_GO_CASH

    def test_chance_send_to_jail(
        self,
        localhost_fake_player: host.LocalHost,
        chance_card: card.ChanceCard,
        fake_player: Player,
        monkeypatch: pytest.MonkeyPatch,
        chance_pos: int,
    ):
        self.set_up(
            fake_player, chance_pos, chance_card, Action.SEND_TO_JAIL, monkeypatch
        )

        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
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
        chance_pos: int,
        monkeypatch: pytest.MonkeyPatch,
    ):
        self.set_up(fake_player, chance_pos, chance_card, action, monkeypatch)

        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)
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
        chance_pos: int,
        monkeypatch: pytest.MonkeyPatch,
    ):
        self.set_up(fake_player, chance_pos, chance_card, action, monkeypatch)

        end_turn = localhost_fake_player._handle_space_trigger(player_uid=0)

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
        chance_pos: int,
        monkeypatch: pytest.MonkeyPatch,
    ):
        self.set_up(
            localhost_middle.game.players[1],
            chance_pos,
            chance_card,
            action,
            monkeypatch,
        )

        player = localhost_middle.game.players[1]
        old_cash = player.cash

        end_turn = localhost_middle._handle_space_trigger(player_uid=1)

        assert end_turn is False
        assert player.cash == old_cash - house_fee * 4 - hotel_fee * 1
