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
        elif event.event_type is EventType.V_BUY_PROPERTY:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.buy_property(self.user_to_player[user_id])
        elif event.event_type is EventType.V_AUCTION_PROPERTY:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.auction_property(self.user_to_player[user_id])
        elif event.event_type in (
            EventType.V_BID_1,
            EventType.V_BID_10,
            EventType.V_BID_50,
            EventType.V_BID_100,
            EventType.V_BID_PASS,
        ):
            msg = event.message
            user_id = msg["user_id"]
            if event.event_type is EventType.V_BID_1:
                amount = 1
            elif event.event_type is EventType.V_BID_10:
                amount = 10
            elif event.event_type is EventType.V_BID_50:
                amount = 50
            elif event.event_type is EventType.V_BID_100:
                amount = 100
            else:
                amount = 0
            self.game_controller.bid_property(self.user_to_player[user_id], amount)
        elif event.event_type is EventType.V_PAY:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.pay(self.user_to_player[user_id])
        elif event.event_type is EventType.V_PROPERTY_STATUS:
            msg = event.message
            user_id = msg["user_id"]
            self.game_controller.get_property_status(self.user_to_player[user_id])
        elif event.event_type is EventType.V_MORTGAGE:
            msg = event.message
            user_id = msg["user_id"]
            property_id = msg["property_id"]
            self.game_controller.mortgage(self.user_to_player[user_id], property_id)
        elif event.event_type is EventType.V_UNMORTGAGE:
            msg = event.message
            user_id = msg["user_id"]
            property_id = msg["property_id"]
            self.game_controller.unmortgage(self.user_to_player[user_id], property_id)
        elif event.event_type is EventType.V_ADD_HOUSE:
            msg = event.message
            user_id = msg["user_id"]
            property_id = msg["property_id"]
            self.game_controller.add_house(self.user_to_player[user_id], property_id)
        elif event.event_type is EventType.V_SELL_HOUSE:
            msg = event.message
            user_id = msg["user_id"]
            property_id = msg["property_id"]
            self.game_controller.sell_house(self.user_to_player[user_id], property_id)
