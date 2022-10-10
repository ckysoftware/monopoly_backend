import enum
import uuid
from dataclasses import dataclass
from typing import Any, Callable

import constants as c
import event
from game import Game
from game.actions import Action

from . import exceptions as exc

# @dataclass(kw_only=True, slots=True)
# class User:
#     # TODO remove optional and use init=False instead
#     name: str
#     uid: str = field(default_factory=lambda: str(uuid.uuid4()))
#     game_id: Optional[str] = None  # assigned after joining a room
#     player_uid: Optional[int] = None  # assigned after joining a game


class GameState(enum.Enum):
    NOT_STARTED = enum.auto()
    WAIT_FOR_ROLL = enum.auto()
    WAIT_FOR_END_TURN = enum.auto()
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
            ...
            return

        self._space_trigger(player_id)
        # self.state = GameState.WAIT_FOR_END_TURN

    def _space_trigger(self, player_id: int) -> None:
        """trigger space, publish event and change state"""
        space_action = self.game.trigger_space()
        if space_action == Action.ASK_TO_BUY:
            property_ = self.game.current_property
            self.state = GameState.ASK_TO_BUY
            self._publish_ask_to_buy_event(player_id, property_.id)
            # self._handle_buy(player_uid=player_uid)
        elif space_action == Action.PAY_RENT:
            ...
            # self._handle_pay_rent(player_uid=player_uid)
        elif space_action in (Action.DRAW_CHANCE_CARD, Action.DRAW_CC_CARD):
            ...
            # end_turn = self._handle_draw_card(
            #     player_uid=player_uid, action=space_action
            # )
        elif space_action in (Action.CHARGE_INCOME_TAX, Action.CHARGE_LUXURY_TAX):
            ...
            # TODO handle bankrupt
            # self._handle_charge_tax(player_uid=player_uid, action=space_action)
        elif space_action == Action.SEND_TO_JAIL:
            ...
            # print(f"Player {player_name}: Step on jail. Send to jail")
            # end_turn = self._send_player(player_uid=player_uid, position=Position.JAIL)
        elif space_action == Action.NOTHING:
            pass  # catch Nothing so that an else check can be used next
        else:
            raise ValueError(f"Unknown trigger {space_action}")  # pragma: no cover

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

        self._double_roll_state_change()

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
            self._double_roll_state_change()

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

    def _move_player(self, player_id: int, steps: int):
        """move player and publish move event"""
        old_pos = self.game.get_player_position()
        new_pos = self.game.move_player(steps=steps)
        self._publish_move_event(player_id, old_pos, new_pos)
        self._check_go_pass()

    def _check_go_pass(self) -> None:
        """handle go checking for position offset and go cash"""
        go_action = self.game.check_go_pass()

        if go_action is Action.PASS_GO:
            old_cash = self.game.get_player_cash()
            _, player_id = self.game.get_current_player()
            new_cash = self.game.add_player_cash(
                player_uid=player_id, amount=c.CONST_GO_CASH
            )
            old_pos = self.game.get_player_position()
            new_pos = self.game.offset_go_pos()
            self._publish_cash_change_event(player_id, old_cash, new_cash)
            self._publish_move_event(
                player_id, old_pos, new_pos
            )  # only offset position

    def _double_roll_state_change(self) -> None:
        """change state and publish event depending on the double roll state"""
        if self.game.has_double_roll:
            self.state = GameState.WAIT_FOR_ROLL
            self._publish_wait_for_roll_event()
        else:
            self.state = GameState.WAIT_FOR_END_TURN
            self._publish_wait_for_end_turn_event()

    def _end_turn(self):
        """handle next player as well, reset double roll, etc"""
        ...

    def _roll_dice(self):
        # TODO multiple types, dice roll for start turn move, for jail, for initializing player
        """return dice roll and publish dice roll event"""
        dice_1, dice_2 = self.game.roll_dice()
        self._publish_dice_event(dice_1, dice_2)
        return dice_1, dice_2

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
