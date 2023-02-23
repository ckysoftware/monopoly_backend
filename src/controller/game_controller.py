from dataclasses import dataclass

import model


@dataclass(slots=True)
class GameController:
    game_model: model.GameModel

    def add_players(self, user_ids: list[str]) -> dict[str, int]:
        return self.game_model.add_players(user_ids)

    def roll_dice(self):
        # TODO
        ...

    def start_game(self):
        self.game_model.start_game()

    def assign_player_token(self, player_id: int, token: int) -> None:
        self.game_model.assign_player_token(player_id, token)

    def roll_and_move(self, player_id: int) -> None:
        self.game_model.handle_roll_and_move_event(player_id)

    def buy_property(self, player_id: int) -> None:
        self.game_model.handle_buy_event(player_id)

    def auction_property(self, player_id: int) -> None:
        self.game_model.handle_auction_event(player_id)

    def bid_property(self, player_id: int, amount: int) -> None:
        self.game_model.handle_bid_event(player_id, amount)

    def pay(self, player_id: int) -> None:
        self.game_model.handle_pay_event(player_id)

    def end_turn(self, player_id: int) -> None:
        self.game_model.handle_end_turn_event(player_id)

    def get_property_status(self, player_id: int) -> None:
        self.game_model.handle_property_status_event(player_id)

    def mortgage(self, player_id: int, property_id: int) -> None:
        self.game_model.handle_mortgage_event(player_id, property_id)

    def unmortgage(self, player_id: int, property_id: int) -> None:
        self.game_model.handle_unmortgage_event(player_id, property_id)

    def add_house(self, player_id: int, property_id: int) -> None:
        self.game_model.handle_add_house_event(player_id, property_id)

    def sell_house(self, player_id: int, property_id: int) -> None:
        self.game_model.handle_sell_house_event(player_id, property_id)
