import uuid
from dataclasses import dataclass

import event
from game import Game

# @dataclass(kw_only=True, slots=True)
# class User:
#     # TODO remove optional and use init=False instead
#     name: str
#     uid: str = field(default_factory=lambda: str(uuid.uuid4()))
#     game_id: Optional[str] = None  # assigned after joining a room
#     player_uid: Optional[int] = None  # assigned after joining a game


# TODO send event later
@dataclass(slots=True)
class GameModel:
    id: str
    game: Game
    publisher: event.Publisher
    player_to_user: dict[int, str]
    user_to_player: dict[str, int]

    def __init__(self, local: bool) -> None:
        self.id = str(uuid.uuid4())
        self.game = Game()
        self.player_to_user = {}
        self.user_to_player = {}
        if local:
            self.publisher = event.LocalPublisher()

    def register_topic(self, topic: event.Topic) -> None:
        self.publisher.register_topic(topic)

    def add_players(self, user_ids: list[str]) -> dict[str, int]:
        """add user to the game and set up user-player mapping"""
        for user_id in user_ids:
            player_id = self.game.add_player(user_id)
            self.player_to_user[player_id] = user_id
            self.user_to_player[user_id] = player_id
        return self.user_to_player

    def assign_player_token(self, user_id: str, token: int) -> None:
        """assign token to player"""
        self.game.assign_player_token(self.user_to_player[user_id], token=token)

    def handle_start_turn(self):
        """handle what to do after starting the turn"""
        if self.game.check_in_jail():
            ...
        else:
            # self._handle_roll_and_move()
            ...

    def _handle_roll_and_move(self):
        # TODO handle go and offset and cash
        dice_1, dice_2 = self._roll_dice()
        # double_roll_action = self.game.check_double_roll()
        new_pos = self.game.move_player(steps=dice_1 + dice_2)
        _, player_id = self.game.get_current_player()
        self.publisher.publish(
            event.Event(
                event.EventType.move, {"player_id": player_id, "position": new_pos}
            )
        )

    def handle_end_turn(self):
        """handle next player as well"""
        ...

    def _roll_dice(self):
        # TODO multiple types, dice roll for start turn move, for jail, for initializing player
        # TODO send event
        """return dice roll and send event"""
        dice_1, dice_2 = self.game.roll_dice()
        self.publisher.publish(
            event.Event(event.EventType.dice_roll, {"dices": (dice_1, dice_2)})
        )
        return dice_1, dice_2
