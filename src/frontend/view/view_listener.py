from dataclasses import dataclass, field

from event import Event, EventType, Subscriber

from .animator import Animator
from .player_token import PlayerToken


@dataclass(slots=True)
class ViewListener(Subscriber):
    animator: Animator
    player_tokens: dict[str, PlayerToken] = field(default_factory=dict)
    player_to_user: dict[int, str] = field(default_factory=dict)

    def set_player_tokens(self, player_tokens: dict[str, PlayerToken]):
        self.player_tokens = player_tokens

    def _get_player_token(self, player_id: int) -> PlayerToken:
        return self.player_tokens[self.player_to_user[player_id]]

    async def listen(self, event: Event):
        if event.event_type is EventType.G_ADD_PLAYER:
            msg = event.message
            for user_id, player_id in msg["user_to_player"].items():
                self.player_to_user[player_id] = user_id
        elif event.event_type is EventType.G_MOVE:
            msg = event.message
            player_id = msg["player_id"]
            old_pos = msg["old_position"]
            new_pos = msg["new_position"]
            self.animator.enqueue_token_move(
                self._get_player_token(player_id), old_pos, new_pos
            )
