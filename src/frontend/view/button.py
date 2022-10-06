import enum
from typing import Any

import event
import pygame


class ButtonType(enum.auto):
    """Enum for button types"""

    ROLL = enum.auto()
    BUY = enum.auto()
    SELL = enum.auto()
    END = enum.auto()


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        user_id: str,
        button_type: ButtonType,
    ):
        super().__init__()
        self.user_id = user_id
        self.button_type = button_type
        self.event_type = self._get_event_type()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 20)
        self.text = self.font.render(text, True, pygame.Color("black"))

        self.allow: bool = False

        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        if self.allow:
            self.image.fill((200, 200, 200))
        else:
            self.image.fill((100, 100, 100))
        self.image.blit(self.text, (5, 0))

    def handle_click(self) -> event.Event:
        return event.Event(
            self.event_type,
            {"user_id": self.user_id},
        )

    def update_allow(self, allow: bool) -> None:
        self.allow = allow
        self.update()

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)

    def _get_event_type(self) -> event.EventType:
        """return event type from button type"""
        if self.button_type is ButtonType.ROLL:
            return event.EventType.V_ROLL_AND_MOVE
        elif self.button_type is ButtonType.END:
            return event.EventType.V_END_TURN
        elif self.button_type is ButtonType.BUY:
            return event.EventType.V_BUY_PROPERTY
        else:
            raise ValueError("Invalid button type")
