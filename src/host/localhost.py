from dataclasses import dataclass
from typing import Optional

import constants as c
from game import Game, card
from game.actions import Action
from game.positions import Position

from host.user import User


# HACK
def generate_state_dict() -> dict[int, str]:
    data = {
        0: "Next player",
        1: "Waiting for roll",
    }
    return data


@dataclass(kw_only=True, slots=True)
class LocalHost:
    player_to_user: dict[int, str]
    user_to_player: dict[str, int]
    game_state: int
    game: Game
    state_dict: dict[int, str]
    is_double_roll: bool

    def __init__(self, users: list[User]) -> None:
        self.game = Game()
        self.state_dict = generate_state_dict()
        self.player_to_user = {}
        self.user_to_player = {}
        self.is_double_roll = False
        for user in users:
            player_uid = self.game.add_player(user.name)
            self.player_to_user[player_uid] = user.uid
            self.user_to_player[user.uid] = player_uid

    def assign_player_token(self, user: User, token: int) -> None:
        self.game.assign_player_token(
            player_uid=self.user_to_player[user.uid], token=token
        )

    def start_game(self) -> dict[int, tuple[int, ...]]:
        self.game.initialize_game_map()
        dice_rolls = self.game.initialize_first_player()
        self.game_state = 1
        print("Game started")
        print("Initial dice rolls for deciding playing orders are:")
        for player_uid, dice_roll in dice_rolls.items():
            print(
                f"Player {self.game.players[player_uid].name}: dice_1 is {dice_roll[0]}, "
                + f"dice_2 is {dice_roll[1]}, sum is {dice_roll[0] + dice_roll[1]}"
            )
        cur_name, _cur_uid = self.game.get_current_player()
        print(f"Player {cur_name} is the first player to play.")
        print()
        return dice_rolls

    def loop(self):
        while True:
            print(f"Current game state: {self.state_dict[self.game_state]}")

            # TODO add function to handle roll
            if self.game_state == 0:
                self._reset_for_next_player()
            elif self.game_state == 1:
                self._start_turn()
                # print(f"Is double: {is_double}")

    def _reset_for_next_player(self) -> None:
        """
        Reset for next player
        """
        # TODO need to think about if double roll can be resetted correctly
        self.game.next_player_and_reset()
        self.game_state = 1  # TODO need to think about how to handle jailed player
        self.is_double_roll = False
        print()

    def _end_turn(self) -> None:
        self.game_state = 0

    def _send_to_jail_and_end_turn(self, player_uid: int) -> None:
        # TODO send to jail doesnt end turn? check this
        # probably end turn need ask mortgage, build those...
        self.game.send_to_jail(player_uid=player_uid)
        self._end_turn()

    def _start_turn(self) -> None:
        player_name, player_uid = self.game.get_current_player()
        move_action, steps = self._handle_movement()
        if move_action == Action.SEND_TO_JAIL:
            print(
                f"Player {player_name}: Rolled double for three times in a row. Send to jail."
            )
            self._send_to_jail_and_end_turn(player_uid=player_uid)
            return

        self._move_player_and_check_go(steps=steps)

        space_action = self.game.trigger_space(player_uid=player_uid)
        print(f"Player {player_name}: action is {space_action}")
        if space_action == Action.ASK_TO_BUY:
            self._handle_buy()
        elif space_action == Action.PAY_RENT:
            ...
        elif space_action in (Action.DRAW_CHANCE_CARD, Action.DRAW_CC_CARD):
            ...
        elif space_action in (Action.CHARGE_INCOME_TAX, Action.CHARGE_LUXURY_TAX):
            # TODO handle bankrupt
            self._handle_charge_tax(action=space_action)
        elif space_action == Action.SEND_TO_JAIL:
            print(f"Player {player_name}: Step on jail. Send to jail")
            self._send_to_jail_and_end_turn(player_uid=player_uid)
            return
        elif space_action == Action.NOTHING:
            pass  # catch Nothing so that a else check can be used next
        else:
            raise ValueError(f"Unknown action for space trigger {space_action}")

        if move_action == Action.ASK_TO_ROLL:
            print(f"Player {player_name}: Rolled double. There is an extra roll.")
            self._start_turn()
        else:
            self._end_turn()

    def _handle_draw_card(self, action: Action) -> None:
        player_name, player_uid = self.game.get_current_player()
        if action == Action.DRAW_CHANCE_CARD:
            drawn_card = self.game.draw_chance_card()
        elif action == Action.DRAW_CC_CARD:
            drawn_card = self.game.draw_cc_card()
        else:
            raise ValueError(f"Unknown action {action} in draw card")
        print(f"Player {player_name}: Draw {drawn_card}")
        self._process_chance_card(player_uid=player_uid, drawn_card=drawn_card)

    def _process_chance_card(self, player_uid: int, drawn_card: card.ChanceCard):
        card_action = drawn_card.trigger()

        match card_action:
            # chance card
            case Action.SEND_TO_BOARDWLAK:
                _new_pos = self._move_player_to_pos(
                    player_uid, position=Position.BOARDWLAK
                )
            case Action.SEND_TO_GO:
                ...
            case Action.SEND_TO_ILLINOIS_AVE:
                ...
            case Action.SEND_TO_ST_CHARLES_PLACE:
                ...
            case Action.SEND_TO_NEAREST_RAILROAD:
                ...
            case Action.SEND_TO_NEAREST_UTILITY:
                ...
            case Action.COLLECT_DIVIDEND:
                ...
            case Action.COLLECT_JAIL_CARD:
                ...
            case Action.SEND_BACK_THREE_SPACES:
                ...
            case Action.SEND_TO_JAIL:
                ...
            case Action.CHARGE_GENERAL_REPAIR_FEE:
                ...
            case Action.CHARGE_POOR_TAX:
                ...
            case Action.SEND_TO_READING_RAILROAD:
                ...
            case Action.PAY_CHAIRMAN_FEE:
                ...
            case Action.COLLECT_LOAN:
                ...
            # CC card
            case Action.COLLECT_BANK_ERROR:
                ...
            case Action.CHARGE_DOCTOR_FEE:
                ...
            case Action.COLLECT_STOCK_SALE:
                ...
            case Action.COLLECT_GRAND_OPERA_NIGHT:
                ...
            case Action.COLLECT_HOLIDAY_FUND:
                ...
            case Action.COLLECT_TAX_REFUND:
                ...
            case Action.COLLECT_BIRTHDAY:
                ...
            case Action.COLLECT_INSURANCE:
                ...
            case Action.CHARGE_HOSPITAL_FEE:
                ...
            case Action.CHARGE_SCHOOL_FEE:
                ...
            case Action.COLLECT_CONSULTANCY_FEE:
                ...
            case Action.CHARGE_STREET_REPAIR_FEE:
                ...
            case Action.COLLECT_CONTEST_PRIZE:
                ...
            case Action.COLLECT_INHERITANCE:
                ...
            case _:
                raise ValueError(f"Unknown action {card_action} in chance card")

    def _handle_buy(self) -> None:
        player_name, player_uid = self.game.get_current_player()
        property_name = self.game.get_space_name(player_uid=player_uid)
        space_details = self.game.get_space_details(player_uid=player_uid)
        print(f"Player {player_name}: Landed on property {property_name}.")
        print(f"Details of the property: \n {space_details}")
        choice = ""
        while choice not in ("buy", "auction"):
            choice = input(
                "Type 'buy' to buy or 'auction' to auction the property. Input: "
            ).lower()
        if choice == "buy":
            new_cash = self.game.buy_property(player_uid=player_uid)
            print(
                f"Player {player_name} bought the property {property_name} for {space_details['price']}."
            )
            print(f"Player {player_name}'s new cash balance is {new_cash}")
        else:
            self._auction_process(player_uid=player_uid)

    def _auction_process(self, player_uid: int) -> None:
        bidders = self.game.auction_property(
            position=self.game.get_player_position(player_uid)
        )
        space_details = self.game.get_space_details(player_uid=player_uid)
        cur_bidder_uid = player_uid
        cur_bid_price = 0
        print(f"Auction for property {space_details['name']} starts.")
        while len(bidders) > 1:
            print(f"Active bidders: {[b.name for b in bidders]}")
            cur_bidder_name, cur_bidder_uid = self.game.get_next_player(cur_bidder_uid)

            bid_choice = ""
            while bid_choice not in (
                "bid 1",
                "bid 10",
                "bid 50",
                "bid 100",
                "pass",
            ):
                print(
                    f"Current bidder is {cur_bidder_name}. Current bid is {cur_bid_price}."
                )
                print("Type 'bid 1' to increment the bid by $1")
                print("Type 'bid 10' to increment the bid by $10")
                print("Type 'bid 50' to increment the bid by $50")
                print("Type 'bid 100' to increment the bid by $100")
                print("Type 'pass' to pass")
                bid_choice = input("Input: ").lower()

            if bid_choice[:3] == "bid":
                bid_increment = int(bid_choice[4:])
                cur_bid_price += bid_increment
                print(
                    f"Player {cur_bidder_name} raised the bid by {bid_increment} to {cur_bid_price}."
                )
            else:
                bidders.pop(cur_bidder_uid)
                print(f"Player {cur_bidder_name} passed.")
        # TODO purchase, think about bankrupt
        winner = bidders[0]
        print(
            f"Player {winner.name} won the auction for {space_details['name']} at bid price ${cur_bid_price}."
        )
        new_cash = self.game.buy_property_transaction(
            player=winner, property=self.game.get_property(player_uid=player_uid)
        )
        print(
            f"Player {winner.name} bought the property {space_details['name']} for {cur_bid_price}."
        )
        print(f"Player {winner.name}'s new cash balance is {new_cash}")

    def _handle_movement(self) -> tuple[Action, int]:
        """
        Returns Action (double_roll, jail or nothing) and steps
        """
        self.game.print_map()
        player_name, player_uid = self.game.get_current_player()
        input(
            f"Player {player_name}: Waiting for player to roll the dice... Press Enter to roll..."
        )
        dice_1, dice_2 = self.game.roll_dice()

        action = self.game.check_double_roll(
            player_uid=player_uid, dice_1=dice_1, dice_2=dice_2
        )
        print(f"Player {player_name}: Rolled {dice_1} and {dice_2}")
        return action, dice_1 + dice_2

    def _move_player_to_pos(self, player_uid: int, position: int) -> int:
        new_pos = self.game.move_player(player_uid, position=position)
        return new_pos

    def _move_player_and_check_go(
        self, steps: int, player_uid: Optional[int] = None
    ) -> int:
        if player_uid is None:
            player_name, player_uid = self.game.get_current_player()
        else:
            player_name = self.game.players[player_uid].name

        print(f"Player {player_name}: Move forward {steps} steps.")

        new_pos = self.game.move_player(player_uid=player_uid, steps=steps)
        go_action = self.game.check_go_pass(player_uid=player_uid)
        if go_action == Action.PASS_GO:
            new_cash = self.game.add_player_cash(
                player_uid=player_uid, amount=c.CONST_GO_CASH
            )
            print(
                f"Player {player_name}: Passed GO, receive ${c.CONST_GO_CASH} to ${new_cash}"
            )
            new_pos = self.game.offset_go_pos(player_uid=player_uid)
        print(f"Player {player_name}: Landed on {self.game.get_space_name(new_pos)}")
        return new_pos

    def _handle_charge_tax(self, action: Action) -> None:
        player_name, player_uid = self.game.get_current_player()
        if action == Action.CHARGE_INCOME_TAX:
            new_cash = self.game.sub_player_cash(
                player_uid=player_uid, amount=c.CONST_INCOME_TAX
            )
            print(
                f"Player {player_name}: Charge income tax of ${c.CONST_INCOME_TAX} to ${new_cash}."
            )
        elif action == Action.CHARGE_LUXURY_TAX:
            new_cash = self.game.sub_player_cash(
                player_uid=player_uid, amount=c.CONST_LUXURY_TAX
            )
            print(
                f"Player {player_name}: Charge luxury tax of ${c.CONST_LUXURY_TAX} to ${new_cash}"
            )


if __name__ == "__main__":
    users = [User(name="N 1"), User(name="N 2")]
    localhost = LocalHost(users=users)

    for user in users:
        localhost.assign_player_token(user=user, token=int(user.name[-1]))

    dice_rolls = localhost.start_game()
    localhost.loop()
