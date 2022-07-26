import pygame


class Screen(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super(Screen, self).__init__()
        self.surface: pygame.surface.Surface = pygame.display.set_mode((width, height))
        self.rect: pygame.rect.Rect = self.surface.get_rect()
