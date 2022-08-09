import pygame

# from .button import Button


class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, user_id: str):
        super(PlayerInfo, self).__init__()
        # button_p1 = Button(100, 100, 100, 100, "Player 1")
        self.user_id = user_id
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 20)

        self.cash: int = 0

        self.name_text = self.font.render(self.user_id, True, pygame.Color("black"))
        self.cash_text = self.font.render(
            f"Cash: {str(self.cash)}", True, pygame.Color("black")
        )

        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update_image()

    def draw(self, surface: pygame.surface.Surface) -> None:
        self.update_image()
        surface.blit(self.image, self.rect)

    def update_image(self) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        self.image.fill("white")
        self.image.blit(self.name_text, (5, 0))
        self.image.blit(self.cash_text, (5, 20))

    def set_cash(self, cash: int) -> None:
        if self.cash == cash:
            color = "black"
        elif self.cash > cash:
            color = "red"
        else:
            color = "green"
        self.cash = cash
        self.cash_text = self.font.render(
            f"Cash: {str(self.cash)}", True, pygame.Color(color)
        )
        self.update_image()

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
