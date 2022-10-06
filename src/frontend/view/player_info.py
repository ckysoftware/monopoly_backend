from typing import Any

import pygame

from . import button

# from .button import Button


class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, user_id: str):
        super(PlayerInfo, self).__init__()
        self.user_id = user_id
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 20)

        self.cash: int = 1000
        self.is_current: bool = False

        self.name_text = self.font.render(self.user_id, True, pygame.Color("black"))
        self.cash_text = self.font.render(
            f"Cash: {str(self.cash)}", True, pygame.Color("black")
        )
        self.buttons: list[button.Button] = self._create_buttons(x, y)

        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def _create_buttons(self, x: int, y: int) -> list[button.Button]:
        def _create_roll_button(x: int, y: int) -> button.Button:
            return button.Button(
                x,
                y + 160,
                60,
                40,
                "Roll",
                self.user_id,
                button.ButtonType.ROLL,
            )

        def _create_end_button(x: int, y: int) -> button.Button:
            return button.Button(
                x + 80,
                y + 160,
                60,
                40,
                "End",
                self.user_id,
                button.ButtonType.END,
            )

        def _create_buy_button(x: int, y: int) -> button.Button:
            return button.Button(
                x + 160,
                y + 160,
                60,
                40,
                "Buy",
                self.user_id,
                button.ButtonType.BUY,
            )

        buttons = [
            _create_roll_button(x, y),
            _create_end_button(x, y),
            _create_buy_button(x, y),
        ]
        return buttons

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        if self.is_current:
            self.image.fill("white")
        else:
            self.image.fill("grey")
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
        self.update()

    def set_current(self, user_id: str) -> None:
        """set the current player"""
        if self.user_id == user_id:
            self.is_current = True
        else:
            self.is_current = False
            for button_ in self.buttons:
                button_.update_allow(False)
        self.update()

    def set_allow_roll(self, user_id: str) -> None:
        """update the roll button to allowed"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.ROLL:
                    button_.update_allow(True)
                    return

    def set_allow_end(self, user_id: str) -> None:
        """update the end button to allowed"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.END:
                    button_.update_allow(True)
                    return

    def set_allow_buy(self, user_id: str, price: int) -> None:
        """update the buy button to allowed"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.BUY and self.cash >= price:
                    button_.update_allow(True)
                    return

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
