import enum
from typing import Any, Optional

import pygame

import event


class ButtonType(enum.auto):
    """Enum for button types"""

    ROLL = enum.auto()
    BUY = enum.auto()
    SELL = enum.auto()
    END = enum.auto()
    AUCTION = enum.auto()
    PAY = enum.auto()
    BID_1 = enum.auto()
    BID_10 = enum.auto()
    BID_50 = enum.auto()
    BID_100 = enum.auto()
    BID_PASS = enum.auto()
    PROPERTY_STATUS = enum.auto()
    MORTGAGE = enum.auto()
    UNMORTGAGE = enum.auto()
    ADD_HOUSE = enum.auto()
    SELL_HOUSE = enum.auto()


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
        property_id: Optional[int] = None,
        text_size: int = 20,
    ):
        super().__init__()
        self.user_id = user_id
        self.button_type = button_type
        self.event_type = self._get_event_type()
        self.width = width
        self.height = height
        self.property_id = property_id
        self.font = pygame.font.SysFont("Arial", text_size)
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
            {"user_id": self.user_id, "property_id": self.property_id},
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
        elif self.button_type is ButtonType.AUCTION:
            return event.EventType.V_AUCTION_PROPERTY
        elif self.button_type is ButtonType.BID_1:
            return event.EventType.V_BID_1
        elif self.button_type is ButtonType.BID_10:
            return event.EventType.V_BID_10
        elif self.button_type is ButtonType.BID_50:
            return event.EventType.V_BID_50
        elif self.button_type is ButtonType.BID_100:
            return event.EventType.V_BID_100
        elif self.button_type is ButtonType.BID_PASS:
            return event.EventType.V_BID_PASS
        elif self.button_type is ButtonType.PAY:
            return event.EventType.V_PAY
        elif self.button_type is ButtonType.PROPERTY_STATUS:
            return event.EventType.V_PROPERTY_STATUS
        elif self.button_type is ButtonType.MORTGAGE:
            return event.EventType.V_MORTGAGE
        elif self.button_type is ButtonType.UNMORTGAGE:
            return event.EventType.V_UNMORTGAGE
        elif self.button_type is ButtonType.ADD_HOUSE:
            return event.EventType.V_ADD_HOUSE
        elif self.button_type is ButtonType.SELL_HOUSE:
            return event.EventType.V_SELL_HOUSE
        else:
            raise ValueError("Invalid button type")
