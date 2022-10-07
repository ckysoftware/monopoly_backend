from typing import Optional

import pygame
from constant import coordinate as coor

MAP_PROPERTY_ID_TO_MAP_GRID: dict[int, int] = {
    0: 1,
    1: 3,
    2: 6,
    3: 8,
    4: 9,
    5: 11,
    6: 13,
    7: 14,
    8: 16,
    9: 18,
    10: 19,
    11: 21,
    12: 23,
    13: 24,
    14: 26,
    15: 27,
    16: 29,
    17: 31,
    18: 32,
    19: 34,
    20: 37,
    21: 39,
    101: 5,
    102: 15,
    103: 25,
    104: 35,
    111: 12,
    112: 28,
}


class Board(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int, y: int):
        super(Board, self).__init__()
        image = pygame.image.load("./src/frontend/asset/board-800.jpg").convert()
        self.image: pygame.surface.Surface = pygame.transform.scale(
            image, (width, height)
        )
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.ownership: dict[int, Optional[int]] = self._initialise_ownership()
        self.player_color: dict[
            int, tuple[int, int, int]
        ] = self._initialise_player_color()

    def _initialise_ownership(self) -> dict[int, Optional[int]]:
        return {property_id: None for property_id in MAP_PROPERTY_ID_TO_MAP_GRID.keys()}

    def _initialise_player_color(self) -> dict[int, tuple[int, int, int]]:
        return {
            0: (255, 0, 0),
            1: (0, 255, 0),
            2: (0, 0, 255),
            3: (200, 200, 0),
        }

    def _update_owner_display(self, player_id: int, property_id: int) -> None:
        map_pos = MAP_PROPERTY_ID_TO_MAP_GRID[property_id]
        center: tuple[int, int] = coor.OWNER_INDICATOR[map_pos]
        if 0 <= map_pos <= 10 or 20 <= map_pos <= 30:  # top or bottom
            width = 40
            height = 20
        else:  # left or right
            width = 20
            height = 40
        pygame.draw.rect(
            self.image,
            self.player_color[player_id],
            (center[0] - width // 2, center[1] - height // 2, width, height),
        )

    def update_property_owner(self, player_id: int, property_id: int) -> None:
        self.ownership[property_id] = player_id
        self._update_owner_display(player_id, property_id)
