from typing import Any, Optional

import pygame

from . import button


class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, user_id: str):
        super().__init__()
        self.user_id = user_id
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 20)

        self.cash: int = 1000
        self.num_jail_cards: int = 0
        self.is_current: bool = False

        self.name_text = self.font.render(self.user_id, True, pygame.Color("black"))
        self.cash_text = self.font.render(
            f"Cash: {str(self.cash)}", True, pygame.Color("black")
        )
        self.jail_card_text = self.font.render(
            f"Jail card(s): {str(self.num_jail_cards)}", True, pygame.Color("black")
        )
        self.buttons: list[button.Button] = self._create_buttons(x, y)
        self.bid_buttons: list[button.Button] = self._create_bid_buttons(x, y)

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

        def _create_auction_button(x: int, y: int) -> button.Button:
            return button.Button(
                x + 240,
                y + 160,
                80,
                40,
                "Auction",
                self.user_id,
                button.ButtonType.AUCTION,
            )

        def _create_property_status_button(x: int, y: int) -> button.Button:
            return button.Button(
                x + 330,
                y + 160,
                80,
                40,
                "Status",
                self.user_id,
                button.ButtonType.PROPERTY_STATUS,
            )

        def _create_pay_button(x: int, y: int) -> button.Button:
            return button.Button(
                x,
                y + 105,
                60,
                40,
                "Pay",
                self.user_id,
                button.ButtonType.PAY,
            )

        buttons = [
            _create_roll_button(x, y),
            _create_end_button(x, y),
            _create_buy_button(x, y),
            _create_auction_button(x, y),
            _create_property_status_button(x, y),
            _create_pay_button(x, y),
        ]
        return buttons

    def _create_bid_buttons(self, x: int, y: int) -> list[button.Button]:
        height = y + 50
        bid_buttons = [
            button.Button(
                x,
                height,
                70,
                40,
                "Bid 1",
                self.user_id,
                button.ButtonType.BID_1,
            ),
            button.Button(
                x + 80,
                height,
                70,
                40,
                "Bid 10",
                self.user_id,
                button.ButtonType.BID_10,
            ),
            button.Button(
                x + 160,
                height,
                70,
                40,
                "Bid 50",
                self.user_id,
                button.ButtonType.BID_50,
            ),
            button.Button(
                x + 240,
                height,
                70,
                40,
                "Bid 100",
                self.user_id,
                button.ButtonType.BID_100,
            ),
            button.Button(
                x + 320,
                height,
                70,
                40,
                "Pass",
                self.user_id,
                button.ButtonType.BID_PASS,
            ),
        ]
        return bid_buttons

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        if self.is_current:
            self.image.fill("white")
        else:
            self.image.fill("grey")
        self.image.blit(self.name_text, (5, 0))
        self.image.blit(self.cash_text, (5, 20))
        self.image.blit(self.jail_card_text, (200, 20))

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

    def set_num_jail_card(self, num_jail_cards: int) -> None:
        self.num_jail_cards = num_jail_cards
        self.jail_card_text = self.font.render(
            f"Jail card(s): {str(self.num_jail_cards)}", True, pygame.Color("black")
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
        """set the roll button to allowed if user_id matches"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.ROLL:
                    button_.update_allow(True)
                    return

    def set_allow_end(self, user_id: str) -> None:
        """set the end button to allowed if user_id matches"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.END:
                    button_.update_allow(True)
                    return

    def set_allow_buy_and_auction(self, user_id: str, price: int) -> None:
        """set the buy and auction button to allowed if user_id matches and enough cash"""
        if self.is_current and self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.BUY and self.cash >= price:
                    button_.update_allow(True)
                if button_.button_type is button.ButtonType.AUCTION:
                    button_.update_allow(True)

    def set_allow_bid(self, user_id: str) -> None:
        """set the auction bid button to allowed if user_id matches, otherwise disable"""
        if self.user_id == user_id:
            for button_ in self.bid_buttons:
                button_.update_allow(True)
        else:
            for button_ in self.bid_buttons:
                button_.update_allow(False)

    def set_allow_pay(self, user_id: str, price: int) -> None:
        """set the pay button to allowed if user_id matches"""
        if self.user_id == user_id:
            for button_ in self.buttons:
                if button_.button_type is button.ButtonType.PAY and self.cash >= price:
                    button_.update_allow(True)
                    return

    def set_allow_buttons(
        self,
        roll: Optional[bool] = None,
        end: Optional[bool] = None,
        buy: Optional[bool] = None,
        auction: Optional[bool] = None,
        pay: Optional[bool] = None,
    ) -> None:
        """set the buttons to be allowed or not, does not check for user_id"""
        for button_ in self.buttons:
            if roll is not None and button_.button_type is button.ButtonType.ROLL:
                button_.update_allow(roll)
            if end is not None and button_.button_type is button.ButtonType.END:
                button_.update_allow(end)
            if buy is not None and button_.button_type is button.ButtonType.BUY:
                button_.update_allow(buy)
            if auction is not None and button_.button_type is button.ButtonType.AUCTION:
                button_.update_allow(auction)
            if pay is not None and button_.button_type is button.ButtonType.PAY:
                button_.update_allow(pay)

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
