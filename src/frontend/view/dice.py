import pygame


class Dice(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super(Dice, self).__init__()
        self.width = width
        self.height = height
        self.image: pygame.surface.Surface = pygame.image.load(
            "./src/frontend/asset/dice/dice-six-faces-one.svg"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.fname_map = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
        }

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def set_face(self, face: int) -> None:
        self.image = pygame.image.load(
            f"./src/frontend/asset/dice/dice-six-faces-{self.fname_map[face]}.svg"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
