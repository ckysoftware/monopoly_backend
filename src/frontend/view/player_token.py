import uuid

import pygame
from frontend.constant import coordinate as coor


class PlayerToken(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, token: int):
        super(PlayerToken, self).__init__()
        self.user_id = uuid.uuid4().hex
        self.token = token
        self.image: pygame.surface.Surface = pygame.image.load(
            f"./src/frontend/asset/token/token{token}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.position: int = 0
        self.update_rect()

    def get_position(self) -> int:
        return self.position

    def add_position(self, offset: int) -> None:
        self.position += offset
        self.update_rect()

    def set_position(self, position: int) -> None:
        self.position = position
        self.update_rect()

    def update_rect(self) -> None:
        self.rect.center = coor.MAP_GRID[self.position % len(coor.MAP_GRID)]
