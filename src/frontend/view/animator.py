from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

import pygame

from .dice import Dice
from .player_info import PlayerInfo
from .player_token import PlayerToken
from .screen import Screen


class Drawable(Protocol):
    # TODO remove this (?)
    def draw(self, surface: pygame.surface.Surface) -> Any:
        raise NotImplementedError


class Call:
    """class for handling animation call"""

    def __init__(self, fn: Callable[..., Any], *args: ..., **kwargs: ...):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)


def blank_call(n: int = 1) -> list[Call]:
    # blank call for animation (do nothing)
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
    # draw_sprites: list[Drawable] = field(default_factory=list)

    def set_screen(self, screen: Screen) -> None:
        self.screen = screen

    def set_background_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.background_sprites = sprites
        # self.draw_sprites.append(self.background_sprites)

    def set_token_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.token_sprites = sprites
        # self.draw_sprites.append(self.token_sprites)

    def set_dice_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.dice_sprites = sprites
        # self.draw_sprites.append(self.dice_sprites)

    def set_player_info_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.player_info_sprites = sprites
        # self.draw_sprites.append(self.player_info_sprites)

    def set_button_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.button_sprites = sprites

    # def add_draw_sprites(self, drawable: Drawable) -> None:
    #     self.draw_sprites.append(drawable)

    def enqueue_token_move(
        self, token: PlayerToken, old_position: int, new_position: int
    ) -> None:
        for target_pos in range(old_position, new_position + 1):  # inter steps
            self.queue.append(Call(token.set_position, position=target_pos))
            self.queue.extend(blank_call(3))

    def enqueue_dice_roll(self, dices: tuple[int]) -> None:
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

    def enqueue_waiting_for_roll(self, user_id: str) -> None:
        for player in self.player_info_sprites:
            assert isinstance(player, PlayerInfo)
            self.queue.append(Call(player.set_allow_roll, user_id=user_id))

    def draw(self) -> None:
        """get called every frame to draw"""
        if len(self.queue) > 0:
            call = self.queue.popleft()
            call()

            print("drawn")
            self.background_sprites.draw(self.screen.surface)
            self.token_sprites.draw(self.screen.surface)
            self.dice_sprites.draw(self.screen.surface)
            self.player_info_sprites.draw(self.screen.surface)
            self.button_sprites.draw(self.screen.surface)
            # for drawable in self.draw_sprites:
            #     drawable.draw(self.screen.surface)
