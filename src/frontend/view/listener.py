from dataclasses import dataclass, field

from event import Event, EventType, Subscriber

from .animator import Animator
from .player_token import PlayerToken


@dataclass(slots=True)
class Listener(Subscriber):
    animator: Animator
    player_tokens: dict[int, PlayerToken] = field(default_factory=dict)

    def __init__(self, animator: Animator):
        self.animator = animator

    def assign_player_tokens(self, player_tokens: dict[int, PlayerToken]):
        self.player_tokens = player_tokens

    async def listen(self, event: Event):
        if event.event_type == EventType.move:
            msg = event.message
            player_id = msg["player_id"]
            position = msg["position"]
            self.animator.enqueue_token_move(self.player_tokens[player_id], position)
