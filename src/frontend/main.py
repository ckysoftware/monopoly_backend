import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Board(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int, y: int):
        super(Board, self).__init__()
        image = pygame.image.load("./src/frontend/asset/board-800.jpg").convert()
        self.image: pygame.surface.Surface = pygame.transform.scale(
            image, (width, height)
        )
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class PlayerBoard(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int, y: int):
        super(PlayerBoard, self).__init__()
        self.image: pygame.Surface = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class PlayerToken(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, token: int):
        super(PlayerToken, self).__init__()
        self.image: pygame.surface.Surface = pygame.image.load(
            f"./src/frontend/asset/token/token{token}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect: pygame.rect.Rect = self.image.get_rect()

    def move(self, x: int, y: int):
        self.rect.topleft = (x, y)


class Screen(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super(Screen, self).__init__()
        self.surface: pygame.surface.Surface = pygame.display.set_mode((width, height))
        self.rect: pygame.rect.Rect = self.surface.get_rect()


def init_pygame() -> None:
    pygame.init()


def main():
    init_pygame()
    screen = Screen(1200, 800)
    clock = pygame.time.Clock()
    FPS = 30

    rect = pygame.Rect((0, 0), (32, 32))
    box = pygame.Surface((32, 32))
    box.fill(BLACK)

    board = Board(800, 800, 0, 0)
    player_board = PlayerBoard(400, 800, 800, 0)

    background_sprites = pygame.sprite.Group()
    background_sprites.add([board, player_board])

    token_1 = PlayerToken(128, 128, 1)
    token_2 = PlayerToken(128, 128, 2)

    foreground_sprites = pygame.sprite.Group()
    foreground_sprites.add([token_1, token_2])

    # screen.add_drawable(board)
    # screen.add_drawable(player_board)

    current_token = token_1
    while True:
        clock.tick(FPS)
        # print(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    current_token.rect.move_ip(0, -200)
                elif event.key == pygame.K_s:
                    current_token.rect.move_ip(0, 200)
                elif event.key == pygame.K_a:
                    current_token.rect.move_ip(-200, 0)
                elif event.key == pygame.K_d:
                    current_token.rect.move_ip(200, 0)
                elif event.key == pygame.K_1:
                    current_token = token_1
                elif event.key == pygame.K_2:
                    current_token = token_2

        # screen.fill(BLACK)
        background_sprites.draw(screen.surface)
        foreground_sprites.draw(screen.surface)
        screen.surface.blit(box, rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
