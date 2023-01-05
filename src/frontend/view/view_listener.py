from dataclasses import dataclass, field

from event import Event, EventType, Subscriber

from . import data
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
            self.animator.enqueue_token_move(
                self._get_player_token(msg["player_id"]),
                msg["old_position"],
                msg["new_position"],
            )
        elif event.event_type is EventType.G_DICE_ROLL:
            msg = event.message
            self.animator.enqueue_dice_roll(msg["dices"])
        elif event.event_type is EventType.G_CASH_CHANGE:
            msg = event.message
            self.animator.enqueue_cash_change(
                self.player_to_user[msg["player_id"]], msg["old_cash"], msg["new_cash"]
            )
        elif event.event_type is EventType.G_CURRENT_PLAYER:
            msg = event.message
            self.animator.enqueue_current_player(self.player_to_user[msg["player_id"]])
        elif event.event_type is EventType.G_WAIT_FOR_ROLL:
            msg = event.message
            self.animator.enqueue_wait_for_roll(self.player_to_user[msg["player_id"]])
        elif event.event_type is EventType.G_WAIT_FOR_END_TURN:
            msg = event.message
            self.animator.enqueue_wait_for_end_turn(
                self.player_to_user[msg["player_id"]]
            )
        elif event.event_type is EventType.G_ASK_TO_BUY:
            msg = event.message
            property_data = data.CONST_PROPERTY_DATA[msg["property_id"]]
            self.animator.enqueue_ask_to_buy(
                self.player_to_user[msg["player_id"]], property_data
            )
        elif event.event_type is EventType.G_BUY_PROPERTY:
            msg = event.message
            self.animator.enqueue_buy_property(msg["player_id"], msg["property_id"])
        elif event.event_type is EventType.G_START_AUCTION:
            msg = event.message
            self.animator.enqueue_start_auction(
                msg["property_id"],
            )
        elif event.event_type is EventType.G_CURRENT_AUCTION:
            ...
            msg = event.message
            self.animator.enqueue_current_auction(
                data.CONST_PROPERTY_DATA[msg["property_id"]],
                [self.player_to_user[player_id] for player_id in msg["bidders"]],
                self.player_to_user[msg["player_id"]],
                msg["price"],
            )
        elif event.event_type is EventType.G_END_AUCTION:
            msg = event.message
            self.animator.enqueue_end_auction(
                self.player_to_user[msg["player_id"]],
                data.CONST_PROPERTY_DATA[msg["property_id"]],
                msg["price"],
            )
        elif event.event_type is EventType.G_ASK_FOR_RENT:
            msg = event.message
            self.animator.enqueue_ask_for_rent(
                self.player_to_user[msg["payer_id"]],
                self.player_to_user[msg["payee_id"]],
                msg["rent"],
                data.CONST_PROPERTY_DATA[msg["property_id"]],
            )
        elif event.event_type is EventType.G_DRAW_CHANCE_CARD:
            msg = event.message
            self.animator.enqueue_draw_chance_card(
                self.player_to_user[msg["player_id"]],
                msg["description"],
                msg["ownable"],
            )
        elif event.event_type is EventType.G_CHARGE_TAX:
            msg = event.message
            self.animator.enqueue_charge_tax(
                self.player_to_user[msg["player_id"]],
                msg["tax_amount"],
                msg["tax_type"],
            )
        elif event.event_type is EventType.G_COLLECT_JAIL_CARD:
            msg = event.message
            self.animator.enqueue_collect_jail_card(
                self.player_to_user[msg["player_id"]],
                msg["current_card_amount"],
            )