from dataclasses import dataclass, field

from event import Event, EventType, Subscriber

from .game_controller import GameController


@dataclass(slots=True)
class ControllerListener(Subscriber):
    game_controller: GameController
    user_to_player: dict[str, int] = field(default_factory=dict)

    async def listen(self, event: Event):
        if event.event_type is EventType.V_ADD_PLAYER:
            msg = event.message
            user_ids = msg["user_ids"]
            self.user_to_player = self.game_controller.add_players(user_ids)
        elif event.event_type is EventType.V_ROLL_AND_MOVE:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.roll_and_move(self.user_to_player[user_id])
        elif event.event_type is EventType.V_ASSIGN_TOKEN:
            msg = event.message
            user_id = msg["user_id"]
            token = msg["token"]
            self.game_controller.assign_player_token(
                self.user_to_player[user_id], token
            )
        elif event.event_type is EventType.V_START_GAME:
            self.game_controller.start_game()
        elif event.event_type is EventType.V_END_TURN:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.end_turn(self.user_to_player[user_id])
