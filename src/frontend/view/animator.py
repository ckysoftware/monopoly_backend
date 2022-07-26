from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

import pygame

from .player_token import PlayerToken
from .screen import Screen


class Drawable(Protocol):
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError


class Call:
    """class for handling animation call"""

    def __init__(
        self, fn: Callable[..., Any], drawable: bool = False, *args: ..., **kwargs: ...
    ):
        self.fn = fn
        self.drawable = drawable
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)


def placeholder_call() -> Call:
    return Call(lambda: None)


@dataclass(slots=True)
class Animator:
    queue: deque[Call] = field(default_factory=deque)
    screen: Screen = field(init=False)
    background_sprites: pygame.sprite.Group = field(init=False)
    foreground_sprites: pygame.sprite.Group = field(init=False)

    def set_screen(self, screen: Screen) -> None:
        self.screen = screen

    def set_background_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.background_sprites = sprites

    def set_foreground_sprites(self, sprites: pygame.sprite.Group) -> None:
        self.foreground_sprites = sprites

    def enqueue_token_move(self, token: PlayerToken, position: int) -> None:
        current_pos = token.get_position()
        for target_pos in range(current_pos, position):
            self.queue.append(Call(token.set_position, position=target_pos + 1))
            self.queue.append(
                Call(token.draw, drawable=True, surface=self.screen.surface)
            )
            self.queue.append(placeholder_call())
            self.queue.append(placeholder_call())
            self.queue.append(placeholder_call())

    def draw(self) -> None:
        """get called every frame to draw"""
        if len(self.queue) > 0:
            call = self.queue.popleft()

            if call.drawable:  # if the call is drawable, draw the background first
                self.background_sprites.draw(self.screen.surface)
                self.foreground_sprites.draw(self.screen.surface)
            call()
