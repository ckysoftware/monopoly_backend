from dataclasses import dataclass, field
from typing import Optional

import constants as c

import game.dice as dice
from game import card, data, game_initializer, space
from game.actions import Action
from game.game_map import GameMap, SpaceDetails
from game.player import Player


@dataclass(kw_only=True, slots=True)
class Game:
    game_map: GameMap = field(init=False)
    players: list[Player] = field(default_factory=list)  # sorted by Player.uid
    current_player_uid: int = field(init=False)  # current pos of the player_order
    _roll_double_counter: Optional[tuple[int, int]] = None  # uid, count
    cc_deck: card.Deck = field(init=False)
    chance_deck: card.Deck = field(init=False)
    # TODO handle out of the game players
    # TODO jail_list with uid and count
    # TODO [FUTURE] accept game settings

    def get_current_player(self) -> tuple[str, int]:
        return (self.players[self.current_player_uid].name, self.current_player_uid)

    def get_next_player(self, prev_player_uid: int) -> tuple[str, int]:
        next_player_id = (prev_player_uid + 1) % len(self.players)
        return (self.players[next_player_id].name, next_player_id)

    def get_player_position(self, player_uid: int) -> int:
        return self.players[player_uid].position

    # NOTE be careful with this, it's not tested
    def get_space_name(
        self, position: Optional[int] = None, player_uid: Optional[int] = None
    ) -> str:  # pragma: no cover
        """Return space name given by either position or player_uid to retrieve his/her position"""
        if position is not None:
            return self.game_map.get_space_name(position)
        elif player_uid is not None:
            return self.game_map.get_space_name(self.players[player_uid].position)
        else:
            raise ValueError("Either position or player_uid must be provided")

    # NOTE be careful with this, it's not tested
    def get_space_details(
        self, position: Optional[int] = None, player_uid: Optional[int] = None
    ) -> SpaceDetails:  # pragma: no cover
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

    def _initialize_game_map(self) -> None:
        self.game_map = game_initializer.build_game_map(
            HOUSE_LIMIT=c.CONST_HOUSE_LIMIT, HOTEL_LIMIT=c.CONST_HOTEL_LIMIT
        )

    def _initialize_deck(self) -> None:
        """Initialize the deck for chance cards and community chest"""
        self.cc_deck = card.Deck(name="Community Chest Cards")
        self.cc_deck.shuffle_add_cards(data=data.CONST_CC_CARDS)
        self.chance_deck = card.Deck(name="Chance Cards")
        self.chance_deck.shuffle_add_cards(data=data.CONST_CHANCE_CARDS)

    def initialize(self) -> None:
        """Public API to initialize the whole game"""
        self._initialize_deck()
        self._initialize_game_map()

    # TODO test this
    def draw_chance_card(self) -> card.ChanceCard:
        return self.chance_deck.draw_card()

    # TODO test this
    def draw_cc_card(self) -> card.ChanceCard:
        return self.cc_deck.draw_card()

    # NOTE probably need to break down host into round instance maybe
    # host = trigger game.action, ask -> relay msg
    # game = handle game logic -> apply logic

    def next_player_and_reset(self) -> int:
        """Returns the next player uid and reset the game for next player"""
        _name, self.current_player_uid = self.get_next_player(self.current_player_uid)
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

    def move_player(
        self,
        player_uid: int,
        steps: Optional[int] = None,
        position: Optional[int] = None,
    ) -> int:
        """Move player either by steps or map position"""
        if position is not None:
            new_pos = self.players[player_uid].move(position=position)
        elif steps is not None:
            new_pos = self.players[player_uid].move(steps=steps)
        else:
            raise ValueError("Either steps or position must be provided")
        return new_pos

    def check_go_pass(self, player_uid: int) -> Action:
        if self.players[player_uid].position >= self.game_map.size:
            return Action.PASS_GO
        else:
            return Action.NOTHING

    def offset_go_pos(self, player_uid: int) -> int:
        """Offset player's position by the map size after passing Go"""
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

    def assign_player_token(self, player_uid: int, token: int) -> None:
        for player in self.players:
            if player.token == token:
                raise ValueError("Token is already assigned")
        self.players[player_uid].assign_token(token)

    def buy_property(self, player_uid: int, position: Optional[int] = None) -> int:
        player = self.players[player_uid]
        if position is None:
            position = self.get_player_position(player_uid)
        property_ = self.game_map.map_list[position]

        if not isinstance(property_, space.Property):
            raise ValueError(f"Space is not a Property: {type(property_)}")
        if property_.owner_uid is not None:
            raise ValueError("Property is already owned")
        if player.cash < property_.price:
            raise ValueError(f"Player {player.name} does not have enough cash")

        new_cash = self.buy_property_transaction(player, property_)
        return new_cash

    def auction_property(self, position: int) -> list[Player]:
        """Returns the bidders (active players). Raise error if the property is not auctionable"""
        property_ = self.game_map.map_list[position]

        if not isinstance(property_, space.Property):
            raise ValueError(f"Space is not a Property: {type(property_)}")
        if property_.owner_uid is not None:
            raise ValueError("Property is already owned")

        bidders = self.players.copy()
        return bidders

    def buy_property_transaction(
        self, player: Player, property: space.Property, price: Optional[int] = None
    ) -> int:
        # TODO test monopoly after buying, also no monopoly check
        """Process the purchase transactions. If price is not provided, use the property's price"""
        if price is None:
            price = property.price
        new_cash = player.sub_cash(price)
        player.add_property(property)
        property.assign_owner(player.uid)
        return new_cash

    def get_property(
        self, position: Optional[int] = None, player_uid: Optional[int] = None
    ) -> space.Property:
        """Return Property given by either position or player_uid to retrieve his/her position"""
        if position is not None:
            property_ = self.game_map.map_list[position]
        elif player_uid is not None:
            property_ = self.game_map.map_list[self.get_player_position(player_uid)]
        else:
            raise ValueError("Either position or player_uid must be provided")

        if not isinstance(property_, space.Property):
            raise ValueError(f"Space is not a Property: {type(property_)}")
        assert isinstance(property_, space.Property)
        return property_

    def get_player_house_and_hotel_counts(self, player_uid: int) -> tuple[int, int]:
        """Returns the number of houses and hotels owned by the player (house, hotel)"""
        player = self.players[player_uid]
        house_count = 0
        hotel_count = 0
        for property_ in player.properties:
            if isinstance(property_, space.PropertySpace):
                house_count += property_.no_of_houses
                hotel_count += property_.no_of_hotels
        return house_count, hotel_count

    # NOTE be careful no test
    def print_map(self) -> None:  # pragma: no cover
        """Print the map for debug or localhost"""
        player_pos = {player.position: player.uid for player in self.players}
        for i in range(self.game_map.size):
            if i not in player_pos:
                print("[ ]", end="")
            else:
                print(f"[{player_pos[i]}]", end="")
        print()

    # NOTE be careful no test
    def print_player_info(self) -> None:  # pragma: no cover
        for player in self.players:
            print(f"Player {player.name} - {player.position} - {player.cash}")
