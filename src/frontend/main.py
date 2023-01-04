import pygame
import view

import controller
import model
from event import Event, EventType, LocalPublisher, Topic

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


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

    board = view.Board(800, 800, 0, 0)
    player_board = PlayerBoard(400, 800, 800, 0)

    background_sprites = pygame.sprite.Group()
    background_sprites.add([board, player_board])

    token_list = [view.PlayerToken(64, 64, i + 1) for i in range(4)]
    token_sprites = pygame.sprite.Group()
    token_sprites.add(token_list)

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

    notifcation = view.Notification(140, 500, 280, 150)
    animator.set_notification(notifcation)
    player_info_list = [
        view.PlayerInfo(800, 200 * i, 400, 200, token_list[i].user_id) for i in range(4)
    ]
    player_info_sprites = pygame.sprite.Group()
    player_info_sprites.add(player_info_list)
    animator.set_player_info_sprites(player_info_sprites)

    buttons_list = [button for player in player_info_list for button in player.buttons]
    buttons_list.extend(
        [button for player in player_info_list for button in player.bid_buttons]
    )
    button_sprites = pygame.sprite.Group()
    button_sprites.add(buttons_list)
    animator.set_button_sprites(button_sprites)

    property_info_static = view.PropertyInfo(380, 150, 240, 360, 0)
    animator.set_property_info_static(property_info_static)

    game_model = model.GameModel(local=True)
    game_controller = controller.GameController(game_model)

    game_view_topic = Topic("game_view")
    view_listener = view.ViewListener(animator=animator)
    view_listener.set_player_tokens(
        {token_list[i].user_id: token_list[i] for i in range(4)}
    )
    game_view_topic.register_subscriber(view_listener)
    game_model.register_publisher_topic(game_view_topic)

    view_controller_topic = Topic("view_controller")
    controller_listener = controller.ControllerListener(game_controller)
    view_controller_topic.register_subscriber(controller_listener)
    view_controller_publisher = LocalPublisher()
    view_controller_publisher.register_topic(view_controller_topic)

    view_controller_publisher.publish(
        Event(
            EventType.V_ADD_PLAYER,
            {"user_ids": [token_list[i].user_id for i in range(4)]},
        )
    )
    for i in range(4):
        view_controller_publisher.publish(
            Event(
                EventType.V_ASSIGN_TOKEN,
                {"user_id": token_list[i].user_id, "token": token_list[i].token},
            )
        )
    view_controller_publisher.publish(Event(EventType.V_START_GAME, {}))

    background_sprites.draw(screen.surface)
    token_sprites.draw(screen.surface)
    button_sprites.draw(screen.surface)

    while True:
        clock.tick(FPS)
        # print(pygame.mouse.get_pos())
        # print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_w:
            #         current_token.rect.move_ip(0, -200)
            #     elif event.key == pygame.K_s:
            #         current_token.rect.move_ip(0, 200)
            #     elif event.key == pygame.K_a:
            #         current_token.rect.move_ip(-200, 0)
            #     elif event.key == pygame.K_d:
            #         current_token.rect.move_ip(200, 0)
            #     elif event.key == pygame.K_1:
            #         current_token = token_list[0]
            #         print(f"DEBUG: Current token is {current_token.user_id}")
            #     elif event.key == pygame.K_2:
            #         current_token = token_list[1]
            #         print(f"DEBUG: Current token is {current_token.user_id}")
            #     elif event.key == pygame.K_3:
            #         current_token = token_list[2]
            #         print(f"DEBUG: Current token is {current_token.user_id}")
            #     elif event.key == pygame.K_4:
            #         current_token = token_list[3]
            #         print(f"DEBUG: Current token is {current_token.user_id}")
            #     elif event.key == pygame.K_g:
            #         view_controller_publisher.publish(
            #             Event(
            #                 EventType.V_ROLL_AND_MOVE,
            #                 {"user_id": current_token.user_id},
            #             )
            #         )
            #     elif event.key == pygame.K_z:
            #         view_controller_publisher.publish(
            #             Event(EventType.V_END_TURN, {"user_id": current_token.user_id})
            #         )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button in button_sprites:
                    assert isinstance(button, view.Button)
                    if button.rect.collidepoint(pos):
                        print(f"DEBUG: Button {button.text} clicked")
                        view_controller_publisher.publish(button.handle_click())

        # screen.fill(BLACK)

        # screen.surface.blit(box, rect)
        # background_sprites.draw(screen.surface)
        animator.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
