from dataclasses import dataclass
from typing import Optional

import constants as c
from game import Game
from game.actions import Action

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
        cur_name, _ = self.game.get_current_player()
        print(f"Player {cur_name} is the first player to play.")
        print()
        return dice_rolls

    def loop(self):
        print(f"Current game state: {self.state_dict[self.game_state]}")

        # TODO add function to handle roll
        if self.game_state == 0:
            self._reset_for_next_player()
        elif self.game_state == 1:
            self._start_turn()
            # print(f"Is double: {is_double}")
        self.loop()

    def _reset_for_next_player(self) -> None:
        """
        Reset for next player
        """
        # TODO need to think about if double roll can be resetted correctly
        self.game.next_player()
        self.game_state = 1  # TODO need to think about how to handle jailed player
        self.is_double_roll = False
        print()

    def _send_to_jail(self, player_uid: int) -> None:
        self.game.send_to_jail(player_uid=player_uid)
        self.game_state = 0

    def _start_turn(self) -> None:
        player_name, player_uid = self.game.get_current_player()
        move_action, steps = self._handle_movement()
        if move_action == Action.SEND_TO_JAIL:
            print(
                f"Player {player_name}: Rolled double for three times in a row. Send to jail."
            )
            self._send_to_jail(player_uid=player_uid)
            # NOTE exit point maybe

        self._move_player_and_check_go(steps=steps)

        space_action = self.game.trigger_space(player_uid=player_uid)
        print(f"Player {player_name}: action is {space_action}")
        if space_action == Action.ASK_TO_BUY:
            ...
        elif space_action == Action.START_AUCTION:
            ...
        elif space_action == Action.PAY_RENT:
            ...
        elif space_action == Action.DRAW_CHANCE_CARD:
            ...
        elif space_action == Action.DRAW_CC_CARD:
            ...
        elif space_action in (Action.CHARGE_INCOME_TAX, Action.CHARGE_LUXURY_TAX):
            # TODO handle bankrupt
            self._handle_charge_income_tax(action=space_action)
        elif space_action == Action.SEND_TO_JAIL:
            print(f"Player {player_name}: Step on jail. Send to jail")
            self._send_to_jail(player_uid=player_uid)
        elif space_action == Action.NOTHING:
            pass
        else:
            raise ValueError(f"Unknown action for space trigger {space_action}")

        if move_action == Action.ASK_TO_ROLL:
            print(f"Player {player_name}: Rolled double. There is an extra roll.")
            self._start_turn()
        else:
            self.game_state = 0
        return

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
            new_cash = self.game.add_player_go_cash(player_uid=player_uid)
            print(
                f"Player {player_name}: Passed GO, receive ${c.CONST_GO_CASH} to ${new_cash}"
            )
            new_pos = self.game.offset_go_pos(player_uid=player_uid)
        print(f"Player {player_name}: Landed on {self.game.get_space_details(new_pos)}")
        return new_pos

    def _handle_charge_income_tax(self, action: Action) -> None:
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
