import pygame
from event import Event, EventType, LocalPublisher, Topic

import view

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


def init_pygame() -> None:
    pygame.init()


def main():
    init_pygame()
    screen = view.Screen(1200, 800)
    clock = pygame.time.Clock()
    FPS = 30

    # rect = pygame.Rect((0, 0), (32, 32))
    # box = pygame.Surface((32, 32))
    # box.fill(BLACK)

    board = Board(800, 800, 0, 0)
    player_board = PlayerBoard(400, 800, 800, 0)

    background_sprites = pygame.sprite.Group()
    background_sprites.add([board, player_board])

    token_1 = view.PlayerToken(64, 64, 1)
    token_2 = view.PlayerToken(64, 64, 2)

    foreground_sprites = pygame.sprite.Group()
    foreground_sprites.add([token_1, token_2])

    animator = view.Animator()
    animator.set_screen(screen)
    animator.set_background_sprites(background_sprites)
    animator.set_foreground_sprites(background_sprites)

    topic = Topic("game")

    listener = view.Listener(animator=animator)
    listener.assign_player_tokens({0: token_1, 1: token_2})

    topic.register_subscriber(listener)

    publisher = LocalPublisher()
    publisher.register_topic(topic)

    # screen.add_drawable(board)
    # screen.add_drawable(player_board)

    current_token = token_1
    loc = 0

    background_sprites.draw(screen.surface)
    foreground_sprites.draw(screen.surface)
    cur_player_id = 0
    while True:
        clock.tick(FPS)
        # print(pygame.mouse.get_pos())
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
                # elif event.key == pygame.K_1:
                #     current_token = token_1
                # elif event.key == pygame.K_2:
                #     current_token = token_2
                elif event.key == pygame.K_q:
                    loc += 1
                    foreground_sprites.update(loc)
                elif event.key == pygame.K_e:
                    loc -= 1
                    foreground_sprites.update(loc)
                elif event.key == pygame.K_z:
                    cur_player_id = 0
                elif event.key == pygame.K_x:
                    cur_player_id = 1
                elif event.key == pygame.K_1:
                    publisher.publish(
                        Event(
                            EventType.move, {"player_id": cur_player_id, "position": 1}
                        )
                    )
                elif event.key == pygame.K_2:
                    publisher.publish(
                        Event(
                            EventType.move, {"player_id": cur_player_id, "position": 2}
                        )
                    )
                elif event.key == pygame.K_3:
                    publisher.publish(
                        Event(
                            EventType.move, {"player_id": cur_player_id, "position": 3}
                        )
                    )
                elif event.key == pygame.K_4:
                    publisher.publish(
                        Event(
                            EventType.move, {"player_id": cur_player_id, "position": 4}
                        )
                    )

        # screen.fill(BLACK)

        # screen.surface.blit(box, rect)
        # background_sprites.draw(screen.surface)
        animator.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
