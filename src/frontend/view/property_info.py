from typing import Any

import pygame


class PropertyInfo(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        property_id: int,
    ):
        super().__init__()
        self.property_id = property_id
        self.width = width
        self.height = height
        self.allow = False

        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.allow:
            surface.blit(self.image, self.rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.image.load(
            f"./src/frontend/asset/property/{self.property_id}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update_allow(self, allow: bool) -> None:
        self.allow = allow

    def update_property(self, property_id: int) -> None:
        self.property_id = property_id
        self.update()

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
