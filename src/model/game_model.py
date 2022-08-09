import enum
import uuid
from dataclasses import dataclass
from typing import Any, Callable

import constants as c
import event
from game import Game
from game.actions import Action

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


def require_current_player(fn: Callable[..., Any]):
    def inner(*args: Any, **kwargs: Any) -> Any | None:
        model = args[0]
        player_id = args[1]
        if player_id != model.game.get_current_player()[1]:
            print("The requesting player does not match with the current player")
        else:
            return fn(*args, **kwargs)

    return inner


# TODO send event later
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

    @require_current_player
    def end_turn(self, player_id: int) -> None:
        # TODO end turn and start next turn and send event for control
        print("player:", self.game.get_current_player()[1])
        self.game.next_player_and_reset()
        self.state = GameState.WAIT_FOR_ROLL
        print("player:", self.game.get_current_player()[1])

    def handle_start_turn(self):
        """handle what to do after starting the turn"""
        # TODO tell view to use jail card or what
        if self.game.check_in_jail():
            ...
        else:
            self._handle_roll_and_move()
            ...

    @require_current_player
    def _handle_roll_and_move(self, player_id: int):
        # TODO handle double roll
        if self.state is not GameState.WAIT_FOR_ROLL:
            raise ValueError("The game is not waiting for roll")

        dice_1, dice_2 = self._roll_dice()
        self.publisher.publish(create_dice_event(dice_1, dice_2))
        double_roll_action = self.game.check_double_roll(dice_1, dice_2)
        old_pos = self.game.get_player_position()
        new_pos = self.game.move_player(steps=dice_1 + dice_2)
        self.publisher.publish(create_move_event(player_id, old_pos, new_pos))
        self._check_go_pass()
        if double_roll_action is Action.ASK_TO_ROLL:
            self.state = GameState.WAIT_FOR_ROLL
            print("DOUBLED")
        elif double_roll_action is Action.SEND_TO_JAIL:
            ...
        else:
            self.state = GameState.WAIT_FOR_END_TURN

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
            self.publisher.publish(
                create_cash_change_event(player_id, old_cash, new_cash)
            )
            self.publisher.publish(create_move_event(player_id, old_pos, new_pos))

    def handle_end_turn(self):
        """handle next player as well"""
        ...

    def _roll_dice(self):
        # TODO multiple types, dice roll for start turn move, for jail, for initializing player
        # TODO send event
        """return dice roll and send event"""
        dice_1, dice_2 = self.game.roll_dice()
        self.publisher.publish(create_dice_event(dice_1, dice_2))
        return dice_1, dice_2


def create_move_event(
    player_id: int, old_position: int, new_position: int
) -> event.Event:
    """create a move event"""
    return event.Event(
        event.EventType.G_MOVE,
        {
            "player_id": player_id,
            "old_position": old_position,
            "new_position": new_position,
        },
    )


def create_cash_change_event(
    player_id: int, old_cash: int, new_cash: int
) -> event.Event:
    """create a cash change event"""
    return event.Event(
        event.EventType.G_CASH_CHANGE,
        {"player_id": player_id, "old_cash": old_cash, "new_cash": new_cash},
    )


def create_dice_event(dice_1: int, dice_2: int) -> event.Event:
    """create a dice event"""
    return event.Event(event.EventType.G_DICE_ROLL, {"dices": (dice_1, dice_2)})
