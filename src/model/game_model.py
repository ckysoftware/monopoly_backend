import enum
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Optional

import constants as c
import event
from game import Game, card
from game import positions as pos
from game.actions import Action

from . import exceptions as exc

# @dataclass(kw_only=True, slots=True)
# class User:
#     name: str
#     uid: str = field(default_factory=lambda: str(uuid.uuid4()))
#     game_id: Optional[str] = None  # assigned after joining a room
#     player_uid: Optional[int] = None  # assigned after joining a game


class GameState(enum.Enum):
    NOT_STARTED = enum.auto()
    WAIT_FOR_ROLL = enum.auto()
    WAIT_FOR_END_TURN = enum.auto()
    WAIT_FOR_PAY_RENT = enum.auto()
    ASK_TO_BUY = enum.auto()
    AUCTION = enum.auto()


def require_current_player(fn: Callable[..., Any]):
    def inner(*args: Any, **kwargs: Any) -> Any | None:
        model = args[0]
        player_id = args[1]
        if player_id != model.game.get_current_player()[1]:
            raise exc.NotCurrentPlayerError(player_id)
        else:
            return fn(*args, **kwargs)

    return inner


@dataclass(slots=True)
class GameModel:
    id: str
    game: Game
    state: GameState
    publisher: event.Publisher

    def __init__(self, local: bool) -> None:
        self.id = uuid.uuid4().hex
        self.game = Game()
        self.state = GameState.NOT_STARTED
        if local:
            self.publisher = event.LocalPublisher()

    def register_publisher_topic(self, topic: event.Topic) -> None:
        self.publisher.register_topic(topic)

    def add_players(self, user_ids: list[str]) -> dict[str, int]:
        """add user to the game and set up user-player mapping"""
        user_to_player: dict[str, int] = {}
        for user_id in user_ids:
            player_id = self.game.add_player(user_id)
            user_to_player[user_id] = player_id
        self.publisher.publish(
            event.Event(
                event.EventType.G_ADD_PLAYER, {"user_to_player": user_to_player}
            )
        )
        return user_to_player

    def assign_player_token(self, player_id: int, token: int) -> None:
        """assign token to player"""
        if self.state is not GameState.NOT_STARTED:
            raise ValueError("Cannot assign token after the game has already started")
        self.game.assign_player_token(player_id, token=token)

    def start_game(self) -> None:
        if self.state is not GameState.NOT_STARTED:
            raise ValueError("The game has already started")
        self.game.initialize()
        self.game.initialize_first_player()
        self.state = GameState.WAIT_FOR_ROLL
        self._publish_current_player_event()
        # TODO send data about current states of the game and initialize view, and send first player roll_result

    @require_current_player
    def handle_end_turn_event(self, player_id: int) -> None:
        """receive input from player and handle end turn"""
        if self.state is not GameState.WAIT_FOR_END_TURN:
            raise exc.CommandNotMatchingStateError(
                "The game is not waiting for end turn"
            )
        # TODO end turn and start next turn and send event for control
        print("player:", self.game.get_current_player()[1])
        self.game.next_player_and_reset()
        # self.state = GameState.WAIT_FOR_ROLL
        print("player:", self.game.get_current_player()[1])
        # TODO may need to handle the queue for building houses and stuff
        self.start_turn()

    def start_turn(self):
        """Publish event for current player and publish whether the player is in jail or can roll"""
        # TODO tell view to use jail card or what
        self._publish_current_player_event()
        if self.game.check_in_jail():
            ...
        else:
            self.state = GameState.WAIT_FOR_ROLL
            self._publish_wait_for_roll_event()

    @require_current_player
    def handle_roll_and_move_event(self, player_id: int):
        """receive input from player and handle roll and move"""
        if self.state is not GameState.WAIT_FOR_ROLL:
            raise exc.CommandNotMatchingStateError("The game is not waiting for roll")

        dice_1, dice_2 = self._roll_dice()
        double_roll_action = self.game.check_double_roll(dice_1, dice_2)
        self._move_player(player_id, dice_1 + dice_2)

        if double_roll_action is Action.SEND_TO_JAIL:
            self._send_to_jail()
            return
        self._space_trigger()

    def _space_trigger(self) -> None:
        """trigger space, publish event and change state"""
        space_action = self.game.trigger_space()
        if space_action == Action.ASK_TO_BUY:
            self._ask_for_buy()
        elif space_action == Action.PAY_RENT:
            self._ask_for_rent()
        elif space_action in (Action.DRAW_CHANCE_CARD, Action.DRAW_CC_CARD):
            self._draw_chance_card(space_action)
        elif space_action in (Action.CHARGE_INCOME_TAX, Action.CHARGE_LUXURY_TAX):
            # TODO handle bankrupt
            self._charge_tax(tax_action=space_action)
        elif space_action == Action.SEND_TO_JAIL:
            self._send_to_jail()
        elif space_action == Action.NOTHING:
            self._check_double_roll_or_end()
        else:
            raise ValueError(f"Unknown trigger {space_action}")

    def _ask_for_buy(self):
        self.state = GameState.ASK_TO_BUY
        self._publish_ask_to_buy_event(
            self.game.current_player_id, self.game.current_property.id
        )

    def _draw_chance_card(self, action: Action):
        if action is Action.DRAW_CHANCE_CARD:
            drawn_card = self.game.draw_chance_card()
        elif action is Action.DRAW_CC_CARD:
            drawn_card = self.game.draw_cc_card()
        else:
            raise ValueError(f"Unknown action {action} in draw chance card")
        self._publish_draw_chance_card_event(self.game.current_player_id, drawn_card)
        self._process_chance_card(drawn_card)

    def _process_chance_card(self, drawn_card: card.ChanceCard):
        card_action = drawn_card.trigger()
        player_id = self.game.current_player_id
        match card_action:
            case Action.SEND_TO_BOARDWALK:
                self._send_player(position=pos.Position.BOARDWALK)
            case Action.SEND_TO_GO:
                self._send_player(position=pos.Position.GO)
            case Action.SEND_TO_ILLINOIS_AVE:
                self._send_player(position=pos.Position.ILLINOIS_AVE)
            case Action.SEND_TO_ST_CHARLES_PLACE:
                self._send_player(position=pos.Position.ST_CHARLES_PLACE)
            case Action.SEND_TO_NEAREST_RAILROAD:
                self._send_player(position=pos.Position.RAILROADS)
            case Action.SEND_TO_NEAREST_UTILITY:
                self._send_player(position=pos.Position.UTILITIES)
            case Action.COLLECT_DIVIDEND:
                self._change_player_cash(player_id, c.CONST_COLLECT_DIVIDEND)
                self._check_double_roll_or_end()
            case Action.COLLECT_JAIL_CARD:
                # TODO
                raise NotImplementedError
                # self.game.add_player_jail_card(
                #     player_uid=player_uid, jail_card=drawn_card
                # )
                # jail_card_ids = self.game.get_player_jail_card_ids(
                #     player_uid=player_uid
                # )
                # print(
                #     f"Player {player_name} has {len(jail_card_ids)} Get out of Jail Free cards"
                # )
            case Action.SEND_BACK_THREE_SPACES:
                self._move_player(player_id, steps=-3)
                self._space_trigger()
            case Action.SEND_TO_JAIL:
                self._send_to_jail()
            case Action.CHARGE_GENERAL_REPAIR_FEE:
                house_count, hotel_count = self.game.get_player_house_and_hotel_counts(
                    player_id
                )
                charge_amount = (
                    house_count * c.CONST_GENERAL_REPAIR_HOUSE
                    + hotel_count * c.CONST_GENERAL_REPAIR_HOTEL
                )
                self._change_player_cash(player_id, -charge_amount)
                self._check_double_roll_or_end()
            case Action.CHARGE_POOR_TAX:
                self._change_player_cash(player_id, -c.CONST_POOR_TAX)
                self._check_double_roll_or_end()
            case Action.SEND_TO_READING_RAILROAD:
                self._send_player(position=pos.Position.READING_RAILROAD)
            case Action.PAY_CHAIRMAN_FEE:
                # TODO remove inactive players
                charge_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_id:
                        charge_amount += c.CONST_CHAIRMAN_FEE
                        self._change_player_cash(o_player.uid, c.CONST_CHAIRMAN_FEE)
                self._change_player_cash(player_id, -charge_amount)
                self._check_double_roll_or_end()
            case Action.COLLECT_LOAN:
                self._change_player_cash(player_id, c.CONST_COLLECT_LOAN)
                self._check_double_roll_or_end()
            # CC card
            case Action.COLLECT_BANK_ERROR:
                self._change_player_cash(player_id, c.CONST_COLLECT_BANK_ERROR)
                self._check_double_roll_or_end()
            case Action.CHARGE_DOCTOR_FEE:
                self._change_player_cash(player_id, -c.CONST_DOCTOR_FEE)
                self._check_double_roll_or_end()
            case Action.COLLECT_STOCK_SALE:
                self._change_player_cash(player_id, c.CONST_COLLECT_STOCK_SALE)
                self._check_double_roll_or_end()
            case Action.COLLECT_GRAND_OPERA_NIGHT:
                receive_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_id:
                        receive_amount += c.CONST_GRAND_OPERA_NIGHT
                        self._change_player_cash(
                            o_player.uid, -c.CONST_GRAND_OPERA_NIGHT
                        )
                self._change_player_cash(player_id, receive_amount)
                self._check_double_roll_or_end()
            case Action.COLLECT_HOLIDAY_FUND:
                self._change_player_cash(player_id, c.CONST_COLLECT_HOLIDAY_FUND)
                self._check_double_roll_or_end()
            case Action.COLLECT_TAX_REFUND:
                self._change_player_cash(player_id, c.CONST_COLLECT_TAX_REFUND)
                self._check_double_roll_or_end()
            case Action.COLLECT_BIRTHDAY:
                receive_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_id:
                        receive_amount += c.CONST_BIRTHDAY
                        self._change_player_cash(o_player.uid, -c.CONST_BIRTHDAY)
                self._change_player_cash(player_id, receive_amount)
                self._check_double_roll_or_end()
            case Action.COLLECT_INSURANCE:
                self._change_player_cash(player_id, c.CONST_COLLECT_INSURANCE)
                self._check_double_roll_or_end()
            case Action.CHARGE_HOSPITAL_FEE:
                self._change_player_cash(player_id, -c.CONST_HOSPITAL_FEE)
                self._check_double_roll_or_end()
            case Action.CHARGE_SCHOOL_FEE:
                self._change_player_cash(player_id, -c.CONST_SCHOOL_FEE)
                self._check_double_roll_or_end()
            case Action.COLLECT_CONSULTANCY_FEE:
                self._change_player_cash(player_id, c.CONST_COLLECT_CONSULTANCY_FEE)
                self._check_double_roll_or_end()
            case Action.CHARGE_STREET_REPAIR_FEE:
                house_count, hotel_count = self.game.get_player_house_and_hotel_counts(
                    player_id
                )
                charge_amount = (
                    house_count * c.CONST_STREET_REPAIR_HOUSE
                    + hotel_count * c.CONST_STREET_REPAIR_HOTEL
                )
                self._change_player_cash(player_id, -charge_amount)
                self._check_double_roll_or_end()
            case Action.COLLECT_CONTEST_PRIZE:
                self._change_player_cash(player_id, c.CONST_COLLECT_CONTEST_PRIZE)
                self._check_double_roll_or_end()
            case Action.COLLECT_INHERITANCE:
                self._change_player_cash(player_id, c.CONST_COLLECT_INHERITANCE)
                self._check_double_roll_or_end()
            case _:  # pragma: no cover
                raise ValueError(f"Unknown action {card_action} in chance card")

    def _send_player(self, position: pos.Position) -> None:
        """Send a player to a position, handle Go check and trigger space.
        Handles nearest railroad or utility too."""
        if position is pos.Position.JAIL:
            self._send_to_jail()
            return
        player_pos = self.game.current_position
        if position is pos.Position.RAILROADS or position is pos.Position.UTILITIES:
            pos_value = self._find_nearest_position(player_pos, position.value)
        else:
            pos_value = position.value
        self._move_player(self.game.current_player_id, position=pos_value)
        self._space_trigger()

    def _send_to_jail(self) -> None:
        self._move_player(self.game.current_player_id, position=pos.Position.JAIL.value)
        self.state = GameState.WAIT_FOR_END_TURN
        self._publish_wait_for_end_turn_event()

    @staticmethod
    def _find_nearest_position(player_pos: int, search_pos: list[int]) -> int:
        """Find the nearest position from search_pos that is ahead of the
        player's current position."""
        for position in search_pos:
            assert position != player_pos, "Impossible for this"  # pragma: no cover
            if player_pos < position:
                return position
        return search_pos[0]  # returns the first one after passing Go

    @require_current_player
    def handle_buy_event(self, player_id: int) -> None:
        """Handle event when a player buy a property after landing on it.
        Add property and cash, and publish events accordingly"""
        if self.state is not GameState.ASK_TO_BUY:
            raise exc.CommandNotMatchingStateError("The game is not asking to buy")
        old_cash = self.game.get_player_cash(player_id)
        new_cash = self.game.buy_property()
        self._publish_cash_change_event(player_id, old_cash, new_cash)
        self._publish_buy_property_event(player_id, self.game.current_property.id)

        self._check_double_roll_or_end()

    @require_current_player
    def handle_auction_event(self, player_id: int) -> None:
        """Handle event when the player decided to auction the landed property"""
        if self.state is not GameState.ASK_TO_BUY:
            raise exc.CommandNotMatchingStateError("The game is not asking to buy")

        self.state = GameState.AUCTION
        property_ = self.game.current_property
        self.game.auction_property(property_)
        self._publish_start_auction_event(property_.id)
        self._publish_current_auction_event(property_.id)

    def handle_bid_event(self, player_id: int, amount: int) -> None:
        """Handle event when the player decided to bid on the property. Amount = 0 if pass"""
        if self.state is not GameState.AUCTION:
            raise exc.CommandNotMatchingStateError("The game is not in auction")
        if player_id != self.game.bidders[0].uid:
            raise exc.NotCurrentBidderError(player_id)

        self.game.bid_property(amount)
        if len(self.game.bidders) != 1:
            self._publish_current_auction_event(self.game.current_property.id)
        else:
            self._end_auction()
            self._check_double_roll_or_end()

    @require_current_player
    def handle_pay_event(self, player_id: int) -> None:
        if self.state not in (GameState.WAIT_FOR_PAY_RENT,):
            raise exc.CommandNotMatchingStateError("The game is not asking for payment")
        if self.state is GameState.WAIT_FOR_PAY_RENT:
            payee_id, rent = self.game.get_pay_rent_info()
            self._transfer_player_cash(player_id, payee_id, rent)
            self._check_double_roll_or_end()

    def _end_auction(self) -> None:
        """Process the transactions related to ending the auction.
        Reset the auction process in Game.
        Publish property and cash events"""
        property_ = self.game.current_bid_property
        assert property_ is not None
        winner = self.game.get_player(self.game.current_bidder_id)
        old_cash = self.game.get_player_cash(winner.uid)
        new_cash = self.game.buy_property_transaction(
            winner, property_, self.game.current_bid_price
        )
        self._publish_end_auction_event(
            winner.uid, property_.id, self.game.current_bid_price
        )
        self._publish_cash_change_event(winner.uid, old_cash, new_cash)
        self._publish_buy_property_event(winner.uid, property_.id)
        self.game.end_auction()

    def _move_player(
        self,
        player_id: int,
        steps: Optional[int] = None,
        position: Optional[int] = None,
    ) -> None:
        """move player and publish move event. Either steps or position must be provided.
        Position will take precedence.
        Send move event and check go pass"""
        old_pos = self.game.get_player_position()
        print(f"***** {steps} {position} *****")
        new_pos = self.game.move_player(steps=steps, position=position)
        self._publish_move_event(player_id, old_pos, new_pos)
        self._check_go_pass()

    def _check_go_pass(self) -> None:
        """handle go checking for position offset and go cash"""
        go_action = self.game.check_go_pass()

        if go_action is Action.PASS_GO:
            player_id = self.game.current_player_id
            self._change_player_cash(player_id, c.CONST_GO_CASH)
            old_pos = self.game.current_position
            new_pos = self.game.offset_go_pos()
            # offset position by the map size
            self._publish_move_event(player_id, old_pos, new_pos)

    def _check_double_roll_or_end(self) -> None:
        """change state and publish event depending on the double roll state"""
        if self.game.has_double_roll:
            self.state = GameState.WAIT_FOR_ROLL
            self._publish_wait_for_roll_event()
        else:
            self.state = GameState.WAIT_FOR_END_TURN
            self._publish_wait_for_end_turn_event()

    def _ask_for_rent(self) -> None:
        """handle rent payment and publish events"""
        # TODO handles not enough money and bankruptcy, mortgage, trade, etc.
        # send pay rent info -> wait input, but also need to handle bankrupt, probably manual bankrupt
        payee_id, rent = self.game.get_pay_rent_info()
        payer_id = self.game.current_player_id
        self._publish_ask_for_rent_event(
            payer_id, payee_id, rent, self.game.current_property.id
        )
        self.state = GameState.WAIT_FOR_PAY_RENT

    def _end_turn(self):
        """handle next player as well, reset double roll, etc"""
        # TODO
        ...

    def _roll_dice(self):
        # TODO multiple types, dice roll for start turn move, for jail, for initializing player
        """return dice roll and publish dice roll event"""
        dice_1, dice_2 = self.game.roll_dice()
        self._publish_dice_event(dice_1, dice_2)
        return dice_1, dice_2

    def _charge_tax(self, tax_action: Action) -> None:
        """Charge income or luxury tax after landding on the tax square"""
        # TODO send out UI event for tax
        # TODO handle not enough money and bankruptcy, mortgage, trade, etc.
        player_id = self.game.current_player_id
        if tax_action == Action.CHARGE_INCOME_TAX:
            self._change_player_cash(player_id, -c.CONST_INCOME_TAX)
        elif tax_action == Action.CHARGE_LUXURY_TAX:
            self._change_player_cash(player_id, -c.CONST_LUXURY_TAX)
        else:
            raise ValueError(f"Invalid tax action: {tax_action}")

    def _change_player_cash(self, player_id: int, amount: int) -> None:
        """Change player cash and publish cash change event. Amount can be negative"""
        old_cash = self.game.get_player_cash(player_id)
        if amount >= 0:
            new_cash = self.game.add_player_cash(player_id, amount)
        else:
            new_cash = self.game.sub_player_cash(player_id, -amount)
        self._publish_cash_change_event(player_id, old_cash, new_cash)

    def _transfer_player_cash(self, payer_id: int, payee_id: int, amount: int) -> None:
        """transfer player cash and publish cash change event. Amount must be positive"""
        if amount < 0:
            raise ValueError("Amount must be positive. Please swap the two.")
        self._change_player_cash(payer_id, -amount)
        self._change_player_cash(payee_id, amount)

    def _publish_move_event(
        self, player_id: int, old_position: int, new_position: int
    ) -> None:
        """publish a move event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_MOVE,
                {
                    "player_id": player_id,
                    "old_position": old_position,
                    "new_position": new_position,
                },
            )
        )

    def _publish_cash_change_event(
        self, player_id: int, old_cash: int, new_cash: int
    ) -> None:
        """publish a cash change event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_CASH_CHANGE,
                {"player_id": player_id, "old_cash": old_cash, "new_cash": new_cash},
            )
        )

    def _publish_dice_event(self, dice_1: int, dice_2: int) -> None:
        """publish a dice roll event"""
        self.publisher.publish(
            event.Event(event.EventType.G_DICE_ROLL, {"dices": (dice_1, dice_2)})
        )

    def _publish_game_state_event(self) -> event.Event:
        """publish a game state event"""
        # TODO send out all states
        ...
        # self.publisher.publish(event.Event(event.EventType.G_ALL_STATES, {"state": self.state}))

    def _publish_current_player_event(self) -> None:
        """publish a current player event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_CURRENT_PLAYER,
                {"player_id": self.game.current_player_id},
            )
        )

    def _publish_wait_for_roll_event(self) -> None:
        """publisih a waiting for roll event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_WAIT_FOR_ROLL,
                {"player_id": self.game.current_player_id},
            )
        )

    def _publish_wait_for_end_turn_event(self) -> None:
        """publish a wait for end turn event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_WAIT_FOR_END_TURN,
                {"player_id": self.game.current_player_id},
            )
        )

    def _publish_ask_to_buy_event(self, player_id: int, property_id: int) -> None:
        """publish a ask to buy event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_ASK_TO_BUY,
                {"player_id": player_id, "property_id": property_id},
            )
        )

    def _publish_buy_property_event(self, player_id: int, property_id: int) -> None:
        """publish a buy property event due to buying landed property"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_BUY_PROPERTY,
                {"player_id": player_id, "property_id": property_id},
            )
        )

    def _publish_start_auction_event(self, property_id: int) -> None:
        """publish a start auction event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_START_AUCTION,
                {
                    "property_id": property_id,
                },
            )
        )

    def _publish_current_auction_event(self, property_id: int) -> None:
        """publish the current bidder and price in auction property"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_CURRENT_AUCTION,
                {
                    "player_id": self.game.current_bidder_id,
                    "bidders": [player.uid for player in self.game.bidders],
                    "property_id": property_id,
                    "price": self.game.current_bid_price,
                },
            )
        )

    def _publish_end_auction_event(
        self, player_id: int, property_id: int, price: int
    ) -> None:
        """publish a end auction event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_END_AUCTION,
                {
                    "player_id": player_id,
                    "property_id": property_id,
                    "price": price,
                },
            )
        )

    def _publish_ask_for_rent_event(
        self, payer_id: int, payee_id: int, rent: int, property_id: int
    ) -> None:
        """publish rent info to ask for rent"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_ASK_FOR_RENT,
                {
                    "payer_id": payer_id,
                    "payee_id": payee_id,
                    "rent": rent,
                    "property_id": property_id,
                },
            )
        )

    def _publish_draw_chance_card_event(
        self, player_id: int, drawn_card: card.ChanceCard
    ) -> None:
        """publish a chance card drawn event"""
        self.publisher.publish(
            event.Event(
                event.EventType.G_DRAW_CHANCE_CARD,
                {
                    "player_id": player_id,
                    "description": drawn_card.description,
                    "ownable": drawn_card.ownable,
                },
            )
        )
