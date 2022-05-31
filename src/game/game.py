from dataclasses import dataclass, field
from typing import Optional

import constants as c

import game.dice as dice
from game import data, game_initializer, space
from game.actions import Action
from game.game_map import GameMap, SpaceDetails
from game.player import Player


@dataclass(kw_only=True, slots=True)
class Game:
    game_map: GameMap = field(init=False)
    players: list[Player] = field(default_factory=list)  # sorted by Player.uid
    current_player_uid: int = field(init=False)  # current pos of the player_order
    _roll_double_counter: Optional[tuple[int, int]] = None  # uid, count
    # TODO jail_list with uid and count
    # TODO [FUTURE] accept game settings

    # TODO test
    def get_current_player(self) -> tuple[str, int]:
        return (self.players[self.current_player_uid].name, self.current_player_uid)

    def get_next_player(self, prev_player_uid: int) -> tuple[str, int]:
        next_player_id = (prev_player_uid + 1) % len(self.players)
        return (self.players[next_player_id].name, next_player_id)

    # TODO test
    def get_player_position(self, player_uid: int) -> int:
        return self.players[player_uid].position

    # TODO test
    def get_space_name(
        self, position: Optional[int] = None, player_uid: Optional[int] = None
    ) -> str:
        """Return space name given by either position or player_uid to retrieve his/her position"""
        if position is not None:
            return self.game_map.get_space_name(position)
        elif player_uid is not None:
            return self.game_map.get_space_name(self.players[player_uid].position)
        else:
            raise ValueError("Either position or player_uid must be provided")

    # TODO test
    def get_space_details(
        self, position: Optional[int] = None, player_uid: Optional[int] = None
    ) -> SpaceDetails:
        """Return space details given by either position or player_uid to retrieve his/her position"""
        if position is not None:
            return self.game_map.get_space_details(position)
        elif player_uid is not None:
            return self.game_map.get_space_details(self.players[player_uid].position)
        else:
            raise ValueError("Either position or player_uid must be provided")

    # TODO test
    def _reset_for_next_player(self) -> None:
        self._roll_double_counter = None

    def add_player(self, name: str):
        new_player = Player(
            name=name, uid=len(self.players), cash=c.CONST_STARTING_CASH
        )
        self.players.append(new_player)
        return new_player.uid

    def initialize_first_player(self) -> dict[int, tuple[int, ...]]:
        """
        returns: dict[player_uid, (roll_1, roll_2)]
        """
        # NOTE roll dice and return, may be difficult for frontend, probably trigger event -> listen
        roll_result: list[
            tuple[int, int, tuple[int, ...]]
        ] = []  # (sum, player_uid, (dice_1, dice_2, ...))
        roll_max = (0, -1)  # (sum, player_uid)
        for player in self.players:
            dice_rolls = dice.roll(num_faces=6, num_dice=2)
            roll_result.append(
                (sum(dice_rolls), player.uid, dice_rolls)
            )  # sum, player_uid, roll_result tuple(int, ...)
            if sum(dice_rolls) > roll_max[0]:  # if same value, first player first
                roll_max = (sum(dice_rolls), player.uid)
        self.current_player_uid = roll_max[1]
        return {x[1]: x[2] for x in roll_result}  # for frontend to show dice result

    def initialize_game_map(self) -> None:
        self.game_map = game_initializer.build_game_map(
            HOUSE_LIMIT=c.CONST_HOUSE_LIMIT, HOTEL_LIMIT=c.CONST_HOTEL_LIMIT
        )

    # NOTE probably need to break down host into round instance maybe
    # host = trigger game.action, ask -> relay msg
    # game = handle game logic -> apply logic

    def next_player(self) -> int:
        """Returns the next player uid and reset the game for next player"""
        _, self.current_player_uid = self.get_next_player(self.current_player_uid)
        self._reset_for_next_player()
        return self.current_player_uid

    def roll_dice(self) -> tuple[int, ...]:
        return dice.roll(num_faces=6, num_dice=2)

    def check_double_roll(self, player_uid: int, dice_1: int, dice_2: int) -> Action:
        if dice_1 == dice_2:
            if self._roll_double_counter is None:  # 1st roll
                self._roll_double_counter = (player_uid, 1)
                return Action.ASK_TO_ROLL
            elif self._roll_double_counter[0] != player_uid:  # Error
                raise ValueError("Roll double counter has not been resetted correctly")
            elif self._roll_double_counter[1] < c.CONST_MAX_DOUBLE_ROLL - 1:  # 2nd roll
                self._roll_double_counter = (
                    player_uid,
                    self._roll_double_counter[1] + 1,
                )
                return Action.ASK_TO_ROLL
            else:  # 3rd roll
                self._roll_double_counter = None
                return Action.SEND_TO_JAIL
        else:  # not double roll
            self._roll_double_counter = None
            return Action.NOTHING

    def move_player(self, player_uid: int, steps: int) -> int:
        return self.players[player_uid].move(steps)

    def check_go_pass(self, player_uid: int) -> Action:
        if self.players[player_uid].position >= self.game_map.size:
            return Action.PASS_GO
        else:
            return Action.NOTHING

    def offset_go_pos(self, player_uid: int) -> int:
        new_pos = self.players[player_uid].offset_position(self.game_map.size)
        return new_pos

    def trigger_space(self, player_uid: int) -> Action:
        action = self.game_map.trigger(self.players[player_uid])
        return action

    def add_player_cash(self, player_uid: int, amount: int) -> int:
        new_cash = self.players[player_uid].add_cash(amount)
        return new_cash

    def sub_player_cash(self, player_uid: int, amount: int) -> int:
        new_cash = self.players[player_uid].sub_cash(amount)
        return new_cash

    # TODO test this
    def assign_player_token(self, player_uid: int, token: int) -> None:
        for player in self.players:
            if player.token == token:
                raise ValueError("Token already assigned")
        self.players[player_uid].assign_token(token)

    # TODO test this
    def send_to_jail(self, player_uid: int) -> None:
        self.players[player_uid].send_to_pos(position=data.PositionMap.JAIL)

    # TODO test this
    def buy_property(self, player_uid: int, position: Optional[int] = None) -> int:
        player = self.players[player_uid]
        if position is None:
            position = self.get_player_position(player_uid)
        property_ = self.game_map.map_list[position]

        if not isinstance(property_, space.Property):
            raise ValueError("Space is not a Property")
        if property_.owner_uid is not None:
            raise ValueError("Property is already owned")
        if player.cash < property_.price:
            raise ValueError(f"Player {player.name} does not have enough cash")

        new_cash = self._buy_property_transaction(player, property_)
        return new_cash

    def auction_property(self, position: int) -> list[Player]:
        property_ = self.game_map.map_list[position]

        if not isinstance(property_, space.Property):
            raise ValueError("Space is not a Property")
        if property_.owner_uid is not None:
            raise ValueError("Property is already owned")

        bidders = self.players.copy()
        return bidders

    # TODO test this
    def _buy_property_transaction(
        self, player: Player, property_: space.Property
    ) -> int:
        new_cash = player.sub_cash(property_.price)
        player.add_property(property_)
        property_.assign_owner(player.uid)
        return new_cash

    # TODO probably no need to test this, should only pass data to host
    def print_map(self) -> None:
        """Print the map for debug or localhost"""
        player_pos = {player.position: player.uid for player in self.players}
        for i in range(self.game_map.size):
            if i not in player_pos:
                print("[ ]", end="")
            else:
                print(f"[{player_pos[i]}]", end="")
        print()

    # TODO probably no need to test this, should only pass data to host
    def print_player_info(self) -> None:
        for player in self.players:
            print(f"Player {player.name} - {player.position} - {player.cash}")
