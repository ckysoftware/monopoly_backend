from dataclasses import dataclass, field

import constants as c

import src.game.dice as dice
from src.game.actions import Action as A
from src.game.game_map import GameMap
from src.game.player import Player


@dataclass(kw_only=True, slots=True)
class Game:
    game_map: GameMap
    players: list[Player] = field(default_factory=list)
    current_player_uid: int = None  # current pos of the player_order
    _roll_double_counter: (int) = None  # tuple(int, int) to store (uid, double_count)

    def add_player(self, name: str):
        new_player = Player(
            name=name, uid=len(self.players), cash=c.CONST_STARTING_CASH
        )
        self.players.append(new_player)
        return new_player.uid

    def initilize_first_player(self) -> dict[int, tuple[int, ...]]:
        # NOTE roll dice and return, may be difficult for frontend, probably trigger event -> listen
        roll_result = []  # (sum, player_uid, (dice_1, dice_2))
        roll_max = (0, -1)  # (sum, player_uid)
        for player in self.players:
            dice_1, dice_2 = dice.roll(num_faces=6, num_dice=2)
            roll_result.append(
                (dice_1 + dice_2, player.uid, (dice_1, dice_2))
            )  # sum, player_uid, roll_result tuple(int, ...)
            if dice_1 + dice_2 > roll_max[0]:  # if same value, first player first
                roll_max = (dice_1 + dice_2, player.uid)
        self.current_player_uid = roll_max[1]
        return {x[1]: x[2] for x in roll_result}  # for frontend to show dice result

    # NOTE probably need to break down host into round instance maybe
    # host = trigger src.game.action, ask -> relay msg
    # game = handle game logic -> apply logic

    # TODO
    def next_player(self) -> int:
        pass

    def roll_dice(self) -> (int):
        return dice.roll(num_faces=6, num_dice=2)

    def check_double_roll(self, player_uid: int, dice_1: int, dice_2: int) -> A:
        if dice_1 == dice_2:
            if self._roll_double_counter is None:  # 1st roll
                self._roll_double_counter = (player_uid, 1)
                return A.ASK_TO_ROLL
            elif self._roll_double_counter[0] != player_uid:  # Error
                raise ValueError("Roll double counter has not been resetted correctly")
            elif self._roll_double_counter[1] < c.CONST_MAX_DOUBLE_ROLL - 1:  # 2nd roll
                self._roll_double_counter = (
                    player_uid,
                    self._roll_double_counter[1] + 1,
                )
                return A.ASK_TO_ROLL
            else:  # 3rd roll
                self._roll_double_counter = None
                return A.SEND_TO_JAIL
        else:  # not double roll
            self._roll_double_counter = None
            return A.NOTHING

    def move_player(self, player_uid: int, steps: int) -> int:
        return self.players[player_uid].move(steps)

    def check_go_pass(self, player_uid: int) -> A:
        if self.players[player_uid].position >= self.game_map.size:
            return A.PASS_GO
        else:
            return A.NOTHING

    def offset_go_pos(self, player_uid: int) -> int:
        new_pos = self.players[player_uid].offset_position(self.game_map.size)
        return new_pos

    def trigger_place(self, player_uid: int) -> A:
        action = self.game_map.trigger(self.players[player_uid])
        return action

    def add_player_cash(self, player_uid: int, amount: int) -> int:
        new_cash = self.players[player_uid].add_cash(amount)
        return new_cash

    def sub_player_cash(self, player_uid: int, amount: int) -> int:
        new_cash = self.players[player_uid].sub_cash(amount)
        return new_cash
