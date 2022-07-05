import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Board(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super(Board, self).__init__()
        self.surface = pygame.image.load("./src/frontend/asset/board-800.jpg").convert()
        self.rect = self.surface.get_rect()
        self.width = width
        self.height = height

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surface, self.rect)


def init_pygame() -> pygame.surface.Surface:
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    return screen


def main():
    screen = init_pygame()
    clock = pygame.time.Clock()
    FPS = 30

    rect = pygame.Rect((0, 0), (32, 32))
    image = pygame.Surface((32, 32))
    image.fill(BLACK)
    board = Board(1200, 800)
    while True:
        clock.tick(FPS)
        print(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rect.move_ip(0, -2)
                elif event.key == pygame.K_s:
                    rect.move_ip(0, 2)
                elif event.key == pygame.K_a:
                    rect.move_ip(-2, 0)
                elif event.key == pygame.K_d:
                    rect.move_ip(2, 0)
        # screen.fill(BLACK)
        board.draw(screen)
        screen.blit(image, rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
