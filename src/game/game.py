from dataclasses import dataclass, field

import constants as c

import game.dice as dice
from game.actions import Action as A
from game.game_map import GameMap
from game.player import Player


@dataclass(kw_only=True, slots=True)
class Game:
    game_map: GameMap
    players: list[Player] = field(default_factory=list)
    current_order_pos: int = None  # current pos of the player_order
    player_order: list[int] = field(default_factory=list)
    _roll_double_counter: (int) = None  # tuple(int, int) to store (uid, double_count)

    def add_player(self, name: str):
        new_player = Player(name=name, uid=len(self.players))
        self.players.append(new_player)
        return new_player.uid

    def initilize_player_order(self) -> dict[int, int]:
        # TODO fix, order should be clockwise starting from the highest player
        # NOTE roll dice and return, may be difficult for frontend, probably trigger event -> listen
        roll_result = []  # (sum, uid, (dice_1, dice_2))
        for player in self.players:
            dice_1, dice_2 = dice.roll(num_faces=6, num_dice=2)
            roll_result.append((dice_1 + dice_2, player.uid, (dice_1, dice_2)))
        sorted_rank = sorted(roll_result)
        self.player_order = [x[1] for x in sorted_rank]
        return {x[1]: x[2] for x in roll_result}  # for frontend to show dice result

    # NOTE probably need to break down host into round instance maybe
    # host = trigger game.action, ask -> relay msg
    # game = handle game logic -> apply logic

    def next_player(self) -> int:
        pass

    def roll_dice(self) -> (int):
        return dice.roll(num_faces=6, num_dice=2)

    def check_double_roll(self, player_uid: int, dice_1: int, dice_2: int) -> A:
        if dice_1 == dice_2:
            if self._roll_double_counter is None:
                self._roll_double_counter = (player_uid, 1)
                return A.ASK_TO_ROLL
            elif self._roll_double_counter[0] != player_uid:
                raise ValueError("Roll double counter has not been resetted correctly")
            elif self._roll_double_counter[1] < c.CONST_MAX_DOUBLE_ROLL - 1:
                self._roll_double_counter = (
                    player_uid,
                    self._roll_double_counter[1] + 1,
                )
                return A.ASK_TO_ROLL
            else:
                self._roll_double_counter = None
                return A.SEND_TO_JAIL
        else:
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
