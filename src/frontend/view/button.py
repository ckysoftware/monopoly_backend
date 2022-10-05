from typing import Any

import event
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, width: int, height: int, text: str, user_id: str, event_type: event.EventType
    ):
        super(Button, self).__init__()
        self.user_id = user_id
        self.event_type = event_type
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 20)
        self.text = self.font.render(text, True, pygame.Color("black"))

        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        self.image.fill((100, 100, 100))
        self.image.blit(self.text, (5, 0))

    def handle_click(self) -> event.Event:
        return event.Event(
            self.event_type,
            {"user_id": self.user_id},
        )

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
