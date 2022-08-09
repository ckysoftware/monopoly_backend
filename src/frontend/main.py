import controller
import model
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

    token_sprites = pygame.sprite.Group()
    token_sprites.add([token_1, token_2])

    dice_1 = view.Dice(100, 100)
    dice_1.update_rect(300, 400)
    dice_2 = view.Dice(100, 100)
    dice_2.update_rect(500, 400)

    dice_sprites = pygame.sprite.Group()
    dice_sprites.add([dice_1, dice_2])

    animator = view.Animator()
    animator.set_screen(screen)
    animator.set_background_sprites(background_sprites)
    animator.set_token_sprites(token_sprites)
    animator.set_dice_sprites(dice_sprites)

    player_info_1 = view.PlayerInfo(800, 0, 400, 250, token_1.user_id)
    player_info_2 = view.PlayerInfo(800, 250, 400, 250, token_2.user_id)
    player_info_sprites = pygame.sprite.Group()
    player_info_sprites.add([player_info_1, player_info_2])
    animator.set_player_info_sprites(player_info_sprites)
    animator.add_draw_sprites(player_info_1)
    animator.add_draw_sprites(player_info_2)

    game_model = model.GameModel(local=True)
    game_controller = controller.GameController(game_model)

    game_view_topic = Topic("game_view")
    view_listener = view.ViewListener(animator=animator)
    view_listener.set_player_tokens(
        {token_1.user_id: token_1, token_2.user_id: token_2}
    )
    game_view_topic.register_subscriber(view_listener)
    game_model.register_publisher_topic(game_view_topic)

    view_controller_topic = Topic("view_controller")
    controller_listener = controller.ControllerListener(game_controller)
    view_controller_topic.register_subscriber(controller_listener)
    view_controller_publisher = LocalPublisher()
    view_controller_publisher.register_topic(view_controller_topic)

    # screen.add_drawable(board)
    # screen.add_drawable(player_board)

    current_token = token_1

    background_sprites.draw(screen.surface)
    token_sprites.draw(screen.surface)

    view_controller_publisher.publish(
        Event(EventType.V_ADD_PLAYER, {"user_ids": [token_1.user_id, token_2.user_id]})
    )
    view_controller_publisher.publish(
        Event(EventType.V_ASSIGN_TOKEN, {"user_id": token_1.user_id, "token": 1})
    )
    view_controller_publisher.publish(
        Event(EventType.V_ASSIGN_TOKEN, {"user_id": token_2.user_id, "token": 2})
    )
    view_controller_publisher.publish(Event(EventType.V_START_GAME, {}))

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
                elif event.key == pygame.K_1:
                    current_token = token_1
                elif event.key == pygame.K_2:
                    current_token = token_2
                elif event.key == pygame.K_g:
                    view_controller_publisher.publish(
                        Event(
                            EventType.V_ROLL_AND_MOVE,
                            {"user_id": current_token.user_id},
                        )
                    )
                elif event.key == pygame.K_z:
                    view_controller_publisher.publish(
                        Event(EventType.V_END_TURN, {"user_id": current_token.user_id})
                    )

        # screen.fill(BLACK)

        # screen.surface.blit(box, rect)
        # background_sprites.draw(screen.surface)
        animator.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
