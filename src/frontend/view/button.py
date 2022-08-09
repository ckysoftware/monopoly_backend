import pygame


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
    ):
        super(Button, self).__init__()
        self.width = width
        self.height = height
        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 20)
        self.text = self.font.render(text, True, pygame.Color("black"))

        self.surface = pygame.Surface(self.text.get_size())
        self.surface.fill("white")
        self.surface.blit(self.text, (0, 0))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
