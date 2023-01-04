from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable

import pygame

from . import data
from .board import Board
from .dice import Dice
from .notification import Notification
from .player_info import PlayerInfo
from .player_token import PlayerToken
from .property_info import PropertyInfo
from .screen import Screen


class Call:
    """class for handling animation call"""

    def __init__(self, fn: Callable[..., Any], *args: ..., **kwargs: ...):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)


def blank_call(n: int = 1) -> list[Call]:
    """blank call for animation (do nothing)"""
    return [Call(lambda: None) for _ in range(n)]


@dataclass(slots=True)
class Animator:
    queue: deque[Call] = field(default_factory=deque)
    screen: Screen = field(init=False)
    background_sprites: pygame.sprite.Group = field(init=False)
    token_sprites: pygame.sprite.Group = field(init=False)
    player_info_sprites: pygame.sprite.Group = field(init=False)
    dice_sprites: pygame.sprite.Group = field(init=False)
    button_sprites: pygame.sprite.Group = field(init=False)
    property_info_static: PropertyInfo = field(init=False)
    notification: Notification = field(init=False)

    def set_screen(self, screen: Screen) -> None:
        self.screen = screen

    def set_background_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.background_sprites = sprites

    def set_token_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.token_sprites = sprites

    def set_dice_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.dice_sprites = sprites

    def set_player_info_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.player_info_sprites = sprites

    def set_button_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.button_sprites = sprites

    def set_property_info_static(self, property_info: PropertyInfo) -> None:
        self.property_info_static = property_info

    def set_notification(self, notification: Notification) -> None:
        self.notification = notification

    def enqueue_token_move(
        self, token: PlayerToken, old_position: int, new_position: int
    ) -> None:
        for target_pos in range(old_position, new_position + 1):  # inter steps
            self.queue.append(Call(token.set_position, position=target_pos))
            self.queue.extend(blank_call(3))

    def enqueue_dice_roll(self, dices: tuple[int]) -> None:
        self._hide_roll_button()
        for sprite, dice in zip(self.dice_sprites, dices):
            assert isinstance(sprite, Dice)
            self.queue.append(Call(sprite.set_face, face=dice))

    def enqueue_cash_change(self, user_id: str, old_cash: int, new_cash: int) -> None:
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            if player.user_id == user_id:
                for inter_cash in range(old_cash, new_cash + 1, 20):  # inter cash
                    self.queue.append(Call(player.set_cash, cash=inter_cash))
                # set final cash, and then change color
                self.queue.append(Call(player.set_cash, cash=new_cash))
                self.queue.append(Call(player.set_cash, cash=new_cash))
                return

    def enqueue_current_player(self, user_id: str) -> None:
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_current, user_id=user_id))

    def enqueue_wait_for_roll(self, user_id: str) -> None:
        self._hide_all_buttons()
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_roll, user_id=user_id))

    def enqueue_wait_for_end_turn(self, user_id: str) -> None:
        self._hide_all_buttons()
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_end, user_id=user_id))

    def enqueue_ask_to_buy(
        self, user_id: str, property_data: data.BasePropertyData
    ) -> None:
        self._hide_roll_button()
        self._show_property_info_static(property_data["id"])
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(
                Call(
                    player.set_allow_buy_and_auction,
                    user_id=user_id,
                    price=property_data["price"],
                )
            )

    def enqueue_buy_property(self, player_id: int, property_id: int) -> None:
        self._hide_buy_and_auction_button()
        self._hide_property_info_static()
        self._update_owner(player_id, property_id)

    def enqueue_start_auction(self, property_id: int) -> None:
        self._hide_buy_and_auction_button()
        self._show_property_info_static(property_id)
        self.queue.append(Call(self.notification.update_allow, True))

    def enqueue_current_auction(
        self,
        property_data: data.BasePropertyData,
        bidders: list[str],
        current_user_id: str,
        price: int,
    ) -> None:
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_bid, user_id=current_user_id))
        noti_text = [
            f"Auction for {property_data['name']} is ongoing.",
            "Active bidders:",
            *[f"    {bidder}" for bidder in bidders],
            f"Current price: {price}.",
        ]
        self.queue.append(Call(self.notification.update, texts=noti_text))

    def enqueue_end_auction(
        self, user_id: str, property_data: data.BasePropertyData, price: int
    ) -> None:
        self._hide_bid_button()
        noti_text = [
            f"{user_id} won the auction.",
            f"Bought {property_data['name']} for ${price}.",
        ]
        self.queue.append(Call(self.notification.update, texts=noti_text))
        # self.queue.append(Call(self.notification.update_allow, False))

    def enqueue_ask_for_rent(
        self,
        payer_id: str,
        payee_id: str,
        rent: int,
        property_data: data.BasePropertyData,
    ) -> None:
        self._hide_roll_button()
        noti_text = [
            f"{payer_id} landed on {payee_id}'s property - {property_data['name']}.",
            f"{payer_id} has to pay ${rent} to {payee_id}.",
        ]
        self.queue.append(Call(self.notification.update, texts=noti_text))

        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_pay, user_id=payer_id, price=rent))

    def enqueue_draw_chance_card(
        self,
        player_id: str,
        description: str,
        ownable: bool,
    ) -> None:
        self._hide_roll_button()
        # TODO change to chance card or CC card
        noti_text = [
            f"{player_id} drew a chance card.",
            description,
        ]
        self.queue.append(Call(self.notification.update, texts=noti_text))
        # TODO add ownable jail card
        # if ownable:
        #     self.queue.append(Call(self.notification.update_allow, True))

    def enqueue_charge_tax(
        self,
        player_id: str,
        tax_amount: int,
        tax_type: str,
    ) -> None:
        noti_text = [f"{player_id} has been charged {tax_type} for {tax_amount}."]
        self.queue.append(Call(self.notification.update, texts=noti_text))

    def _show_property_info_static(self, property_id: int) -> None:
        self.queue.append(Call(self.property_info_static.update_allow, allow=True))
        self.queue.append(
            Call(
                self.property_info_static.update_property,
                property_id=property_id,
            )
        )

    def _hide_property_info_static(self) -> None:
        self.queue.append(Call(self.property_info_static.update_allow, allow=False))

    def _hide_roll_button(self) -> None:
        """hide roll button for all players"""
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_buttons, roll=False))

    def _hide_buy_and_auction_button(self) -> None:
        """hide buy button for all players"""
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_buttons, buy=False, auction=False))

    def _hide_bid_button(self) -> None:
        """hide bid button for all players. Assume no user_id is empty ("")"""
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_bid, ""))

    def _hide_pay_button(self) -> None:
        """hide pay button for all players. Assume no user_id is empty ("")"""
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_pay, pay=False))

    def _hide_all_buttons(self) -> None:
        """hide all buttons for all players"""
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(
                Call(
                    player.set_allow_buttons,
                    roll=False,
                    end=False,
                    buy=False,
                    auction=False,
                    pay=False,
                )
            )

    def _update_owner(self, player_id: int, property_id: int) -> None:
        for background in self.background_sprites:
            if isinstance(background, Board):
                self.queue.append(
                    Call(
                        background.update_property_owner,
                        player_id=player_id,
                        property_id=property_id,
                    )
                )

    def draw(self) -> None:
        """get called every frame to draw"""
        if len(self.queue) > 0:
            call = self.queue.popleft()
            call()

            # print("drawn")
            self.background_sprites.draw(self.screen.surface)
            self.token_sprites.draw(self.screen.surface)
            self.dice_sprites.draw(self.screen.surface)
            self.player_info_sprites.draw(self.screen.surface)
            self.button_sprites.draw(self.screen.surface)
            self.property_info_static.draw(self.screen.surface)
            self.notification.draw(self.screen.surface)
            # for drawable in self.draw_sprites:
            #     drawable.draw(self.screen.surface)
