from dataclasses import dataclass
from typing import Optional

import constants as c
from game import Game, card
from game.actions import Action
from game.enum_types import DeckType
from game.positions import Position

from host.user import User


# HACK
def generate_state_dict() -> dict[int, str]:  # pragma: no cover
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
    is_double_roll: bool  # TODO probably can remove this?
    dice_rolls: Optional[tuple[int, int]]

    def __init__(self, users: list[User]) -> None:
        self.game = Game()
        self.state_dict = generate_state_dict()
        self.player_to_user = {}
        self.user_to_player = {}
        self.is_double_roll = False
        self.dice_rolls = None
        for user in users:
            player_uid = self.game.add_player(user.name)
            self.player_to_user[player_uid] = user.uid
            self.user_to_player[user.uid] = player_uid

    def assign_player_token(self, user: User, token: int) -> None:
        self.game.assign_player_token(
            player_uid=self.user_to_player[user.uid], token=token
        )

    def start_game(self) -> dict[int, tuple[int, ...]]:
        self.game.initialize()
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
        self.dice_rolls = None

    def _start_turn(self) -> None:
        player_name, player_uid = self.game.get_current_player()
        player_jail_turns = self.game.get_player_jail_turns(player_uid)
        if player_jail_turns:
            self._handle_in_jail(player_uid=player_uid, jail_turns=player_jail_turns)
        # TODO probably need a else here or if check on return handle jail
        move_action, steps = self._handle_dice_roll(player_uid=player_uid)
        end_turn = False
        if move_action == Action.SEND_TO_JAIL:
            print(
                f"Player {player_name}: Rolled double for three times in a row. Send to jail."
            )
            end_turn = self._send_player(player_uid, position=Position.JAIL)

        if not end_turn:
            self._move_player_and_check_go(player_uid=player_uid, steps=steps)
            end_turn = self._handle_space_trigger(player_uid=player_uid)

        if not end_turn and move_action == Action.ASK_TO_ROLL:
            # TODO if called recursively by _handle_space_trigger, need to think again
            print(f"Player {player_name}: Rolled double. There is an extra roll.")
            self._start_turn()
        else:
            self._end_turn()

    def _handle_in_jail(self, player_uid: int, jail_turns: int):
        player_name = self.game.players[player_uid].name
        jail_card_ids = self.game.get_player_jail_card_ids(player_uid)
        # TODO handle trade for jail card right after the turn starts
        if len(jail_card_ids) > 0:
            print(
                f"Player {player_name}: You have {len(jail_card_ids)} GET OUT OF JAIL FREE cards."
            )
            while (choice := input("Do you want to use one of them? (y/n)")) not in (
                "y",
                "n",
            ):
                pass
            if choice == "y":
                if len(jail_card_ids) > 1:
                    while (
                        card_in := input(
                            "Do you want to use the one from Chance or Community Chest? (c/cc)"
                        )
                    ) not in ("c", "cc"):
                        ...
                    deck_type = DeckType.CHANCE if card_in == "c" else DeckType.CC
                    _card = self.game.use_player_jail_card(
                        player_uid, deck_type=deck_type
                    )
        # TODO unfinished, pay fine before throwing, throw, add jail turns, if > 3 force fine
        self._handle_dice_roll(player_uid=player_uid)

    def _handle_space_trigger(self, player_uid: int) -> bool:
        """Return True if the player turn has ended, False otherwise"""
        end_turn = False
        player_name = self.game.players[player_uid].name
        space_action = self.game.trigger_space(player_uid=player_uid)
        print(f"Player {player_name}: action is {space_action}")
        if space_action == Action.ASK_TO_BUY:
            self._handle_buy(player_uid=player_uid)
        elif space_action == Action.PAY_RENT:
            self._handle_pay_rent(player_uid=player_uid)
        elif space_action in (Action.DRAW_CHANCE_CARD, Action.DRAW_CC_CARD):
            end_turn = self._handle_draw_card(
                player_uid=player_uid, action=space_action
            )
        elif space_action in (Action.CHARGE_INCOME_TAX, Action.CHARGE_LUXURY_TAX):
            # TODO handle bankrupt
            self._handle_charge_tax(player_uid=player_uid, action=space_action)
        elif space_action == Action.SEND_TO_JAIL:
            print(f"Player {player_name}: Step on jail. Send to jail")
            end_turn = self._send_player(player_uid=player_uid, position=Position.JAIL)
        elif space_action == Action.NOTHING:
            pass  # catch Nothing so that an else check can be used next
        else:
            raise ValueError(f"Unknown trigger {space_action}")  # pragma: no cover
        return end_turn

    def _handle_draw_card(
        self,
        player_uid: int,
        action: Action,
    ) -> bool:
        player_name = self.game.players[player_uid].name
        if action == Action.DRAW_CHANCE_CARD:
            drawn_card = self.game.draw_chance_card()
        elif action == Action.DRAW_CC_CARD:
            drawn_card = self.game.draw_cc_card()
        else:
            raise ValueError(f"Unknown action {action} in draw")  # pragma: no cover
        print(f"Player {player_name}: Drawn {drawn_card.description}")
        return self._process_chance_card(player_uid=player_uid, drawn_card=drawn_card)

    def _process_chance_card(
        self, player_uid: int, drawn_card: card.ChanceCard
    ) -> bool:
        player_name = self.game.players[player_uid].name
        card_action = drawn_card.trigger()
        end_turn = False
        match card_action:
            # chance card
            # TODO in sending, also check do Go check, also check other send in other functions
            case Action.SEND_TO_BOARDWALK:
                end_turn = self._send_player(player_uid, position=Position.BOARDWALK)
            case Action.SEND_TO_GO:
                end_turn = self._send_player(player_uid, position=Position.GO)
            case Action.SEND_TO_ILLINOIS_AVE:
                end_turn = self._send_player(player_uid, position=Position.ILLINOIS_AVE)
            case Action.SEND_TO_ST_CHARLES_PLACE:
                end_turn = self._send_player(
                    player_uid, position=Position.ST_CHARLES_PLACE
                )
            case Action.SEND_TO_NEAREST_RAILROAD:
                end_turn = self._send_player(player_uid, position=Position.RAILROADS)
            case Action.SEND_TO_NEAREST_UTILITY:
                end_turn = self._send_player(player_uid, position=Position.UTILITIES)
            case Action.COLLECT_DIVIDEND:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_DIVIDEND
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_JAIL_CARD:
                self.game.add_player_jail_card(
                    player_uid=player_uid, jail_card=drawn_card
                )
                jail_card_ids = self.game.get_player_jail_card_ids(
                    player_uid=player_uid
                )
                print(
                    f"Player {player_name} has {len(jail_card_ids)} Get out of Jail Free cards"
                )
            case Action.SEND_BACK_THREE_SPACES:
                _ = self.game.move_player(player_uid, steps=-3)
                end_turn = self._handle_space_trigger(player_uid=player_uid)
            case Action.SEND_TO_JAIL:
                end_turn = self._send_player(player_uid, position=Position.JAIL)
            case Action.CHARGE_GENERAL_REPAIR_FEE:
                house_count, hotel_count = self.game.get_player_house_and_hotel_counts(
                    player_uid
                )
                charge_amount = (
                    house_count * c.CONST_GENERAL_REPAIR_HOUSE
                    + hotel_count * c.CONST_GENERAL_REPAIR_HOTEL
                )
                print(
                    f"Charge amount is ${charge_amount} for {house_count} houses and {hotel_count} hotels"
                )
                new_cash = self.game.sub_player_cash(player_uid, amount=charge_amount)
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.CHARGE_POOR_TAX:
                new_cash = self.game.sub_player_cash(
                    player_uid, amount=c.CONST_POOR_TAX
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.SEND_TO_READING_RAILROAD:
                end_turn = self._send_player(
                    player_uid, position=Position.READING_RAILROAD
                )
            case Action.PAY_CHAIRMAN_FEE:
                charge_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_uid:
                        charge_amount += c.CONST_CHAIRMAN_FEE
                        new_cash = self.game.add_player_cash(
                            o_player.uid, amount=c.CONST_CHAIRMAN_FEE
                        )
                        print(
                            f"Player {o_player.name}'s new cash balance is ${new_cash}"
                        )
                new_cash = self.game.sub_player_cash(player_uid, amount=charge_amount)
                print(
                    f"Charge amount is ${charge_amount} for {charge_amount//c.CONST_CHAIRMAN_FEE} people"
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_LOAN:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_LOAN
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            # CC card
            case Action.COLLECT_BANK_ERROR:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_BANK_ERROR
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.CHARGE_DOCTOR_FEE:
                new_cash = self.game.sub_player_cash(
                    player_uid, amount=c.CONST_DOCTOR_FEE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_STOCK_SALE:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_STOCK_SALE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_GRAND_OPERA_NIGHT:
                receive_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_uid:
                        receive_amount += c.CONST_GRAND_OPERA_NIGHT
                        new_cash = self.game.sub_player_cash(
                            o_player.uid, amount=c.CONST_GRAND_OPERA_NIGHT
                        )
                        print(
                            f"Player {o_player.name}'s new cash balance is ${new_cash}"
                        )
                new_cash = self.game.add_player_cash(player_uid, amount=receive_amount)
                print(
                    f"Charge amount is ${receive_amount} for {receive_amount//c.CONST_GRAND_OPERA_NIGHT} people"
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_HOLIDAY_FUND:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_HOLIDAY_FUND
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_TAX_REFUND:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_TAX_REFUND
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_BIRTHDAY:
                receive_amount = 0
                for o_player in self.game.players:
                    if o_player.uid != player_uid:
                        receive_amount += c.CONST_BIRTHDAY
                        new_cash = self.game.sub_player_cash(
                            o_player.uid, amount=c.CONST_BIRTHDAY
                        )
                        print(
                            f"Player {o_player.name}'s new cash balance is ${new_cash}"
                        )
                new_cash = self.game.add_player_cash(player_uid, amount=receive_amount)
                print(
                    f"Charge amount is ${receive_amount} for {receive_amount//c.CONST_BIRTHDAY} people"
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_INSURANCE:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_INSURANCE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.CHARGE_HOSPITAL_FEE:
                new_cash = self.game.sub_player_cash(
                    player_uid, amount=c.CONST_HOSPITAL_FEE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.CHARGE_SCHOOL_FEE:
                new_cash = self.game.sub_player_cash(
                    player_uid, amount=c.CONST_SCHOOL_FEE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_CONSULTANCY_FEE:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_CONSULTANCY_FEE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.CHARGE_STREET_REPAIR_FEE:
                house_count, hotel_count = self.game.get_player_house_and_hotel_counts(
                    player_uid
                )
                charge_amount = (
                    house_count * c.CONST_STREET_REPAIR_HOUSE
                    + hotel_count * c.CONST_STREET_REPAIR_HOTEL
                )
                print(
                    f"Charge amount is ${charge_amount} for {house_count} houses and {hotel_count} hotels"
                )
                new_cash = self.game.sub_player_cash(player_uid, amount=charge_amount)
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_CONTEST_PRIZE:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_CONTEST_PRIZE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case Action.COLLECT_INHERITANCE:
                new_cash = self.game.add_player_cash(
                    player_uid, amount=c.CONST_COLLECT_INHERITANCE
                )
                print(f"Player {player_name}'s new cash balance is ${new_cash}")
            case _:  # pragma: no cover
                raise ValueError(f"Unknown action {card_action} in chance card")
        return end_turn

    def _send_player(self, player_uid: int, position: Position) -> bool:
        """Send a player to a position, handle Go check and trigger space.
        Handles nearest railroad or utility too.
        Returns True if end turn, False otherwise"""
        player_name = self.game.players[player_uid].name
        player_pos = self.game.players[player_uid].position
        if position == Position.JAIL:
            print(f"Player {player_name}: Moves to Jail")
            _ = self._send_to_jail(player_uid)
            return True

        if position == Position.RAILROADS or position == Position.UTILITIES:
            pos_value = self._find_nearest_position(player_pos, position.value)
        else:
            pos_value = position.value
        space_name = self.game.get_space_name(position=pos_value)
        print(f"Player {player_name}: Moves to {space_name}")

        if player_pos >= pos_value:
            new_cash = self.game.add_player_cash(player_uid, amount=c.CONST_GO_CASH)
            print(
                f"Player {player_name}: Passed GO, receive ${c.CONST_GO_CASH} to ${new_cash}"
            )

        _ = self.game.move_player(player_uid, position=pos_value)
        end_turn = self._handle_space_trigger(player_uid=player_uid)
        return end_turn

    def _find_nearest_position(self, player_pos: int, search_pos: list[int]) -> int:
        """Find the nearest position from search_pos that is ahead of the
        player's current position."""
        for pos in search_pos:
            assert pos != player_pos, "Impossible for this case"  # pragma: no cover
            if player_pos < pos:
                return pos
        return search_pos[0]  # returns the first one after passing Go

    def _send_to_jail(self, player_uid: int) -> None:
        # TODO probably should remove this... seems send_player can handle this
        # send to jail doesnt end turn? check this
        # probably end turn need ask mortgage, build house those...
        self.game.move_player(player_uid=player_uid, position=Position.JAIL.value)

    def _handle_buy(self, player_uid: int) -> None:
        """Handle buy or auction for the player_uid.
        If player_uid is None, then get the current player of the game."""
        player_name = self.game.players[player_uid].name
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
            self._handle_auction(player_uid=player_uid)

    def _handle_pay_rent(self, player_uid: int) -> None:
        """Handle pay rent for the player_uid."""
        if self.dice_rolls is None:
            raise ValueError("Dice rolls is None")

        player_name = self.game.players[player_uid].name
        payee_uid, rent = self.game.get_pay_rent_info(
            player_uid=player_uid, dice_count=sum(self.dice_rolls)
        )
        payee_name = self.game.players[payee_uid].name
        print(
            f"Player {player_name} needs to pay rent to Player {payee_name} for ${rent}"
        )
        if self.game.get_player_cash(player_uid) < rent:
            # _handle_not_enough_cash_to_player(player_uid=player_uid)
            raise NotImplementedError
        else:
            new_cash_payer, new_cash_payee = self.game.transfer_cash(
                player_uid, payee_uid, rent
            )
            print(f"Player {player_name}'s new cash balance is ${new_cash_payer}.")
            print(f"Player {payee_name}'s new cash balance is ${new_cash_payee}")

    def _handle_not_enough_cash_to_player(self, player_uid: int):
        # TODO
        """handle the case when the player_uid does not have enough cash to pay
        to other player"""
        ...

    def _handle_not_enough_cash_to_bank(self, player_uid: int):
        # TODO
        """handle the case when the player_uid does not have enough cash to pay
        to the bank"""
        ...

    def _handle_auction(self, player_uid: int) -> None:
        bidders = self.game.auction_property_old(
            position=self.game.get_player_position(player_uid)
        )
        space_details = self.game.get_space_details(player_uid=player_uid)
        cur_bid_price = 0
        print(f"Auction for property {space_details['name']} starts.")
        while len(bidders) > 1:
            print(f"Active bidders: {[b.name for b in bidders]}")
            cur_bidder = bidders[0]

            bid_choice = ""
            while bid_choice not in (
                "bid 1",
                "bid 10",
                "bid 50",
                "bid 100",
                "pass",
            ):
                print(
                    f"Current bidder is {cur_bidder.name}. Current bid is {cur_bid_price}."
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
                    f"Player {cur_bidder.name} raised the bid by {bid_increment} to {cur_bid_price}."
                )
                bidders.rotate(-1)
            else:
                print(f"Player {cur_bidder.name} passed.")
                bidders.popleft()
        # TODO purchase, think about bankrupt
        winner = bidders[0]
        print(
            f"Player {winner.name} won the auction for {space_details['name']} at bid price ${cur_bid_price}."
        )
        new_cash = self.game.buy_property_transaction(
            player=winner,
            property=self.game.get_property(player_uid=player_uid),
            price=cur_bid_price,
        )
        print(
            f"Player {winner.name} bought the property {space_details['name']} for {cur_bid_price}."
        )
        print(f"Player {winner.name}'s new cash balance is {new_cash}")

    def _handle_dice_roll(self, player_uid: int) -> tuple[Action, int]:
        """
        Returns Action (double_roll, jail or nothing) and steps.
        Set attribute dice_rolls.
        """
        self.game.print_map()
        player_name = self.game.players[player_uid].name
        input(
            f"Player {player_name}: Waiting for player to roll the dice... Press Enter to roll..."
        )
        dice_1, dice_2 = self.game.roll_dice()

        action = self.game.check_double_roll(
            player_uid=player_uid, dice_1=dice_1, dice_2=dice_2
        )
        print(f"Player {player_name}: Rolled {dice_1} and {dice_2}")
        self.dice_rolls = (dice_1, dice_2)
        return action, dice_1 + dice_2

    def _move_player_and_check_go(self, player_uid: int, steps: int) -> int:
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

    def _handle_charge_tax(
        self,
        player_uid: int,
        action: Action,
    ) -> None:
        player_name = self.game.players[player_uid].name
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
