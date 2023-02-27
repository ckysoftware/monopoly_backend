from typing import Any, Optional

import pygame

from . import button, data


class PlayerPropertyStatus(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 12)

        self.content: list[list[pygame.surface.Surface | pygame.sprite.Sprite]] = [
            [self.font.render("", True, pygame.Color("black"))]
        ]
        self.allow: bool = False
        self.buttons: list[button.Button] = []
        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def update(
        self,
        property_status: Optional[list[dict[str, Any]]] = None,
        user_id: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))

        if not property_status or not user_id:
            return

        self._process_property_status(property_status)
        self.content: list[list[pygame.surface.Surface | pygame.sprite.Sprite]] = []

        self.buttons = []
        for i, status in enumerate(property_status):
            line = (
                f"{status['name']}"
                # + f" - Houses: {status['num_of_houses']}"
                # + f" - Hotels: {status['num_of_hotels']}"
                # + f" - Price: {status['price_of_house']}"
            )
            self.font.render(line, True, pygame.Color("black"))

            y = i * 20
            action_buttons = self._create_property_buttons(
                y, user_id, status["property_id"]
            )
            self.buttons.extend(action_buttons)

            self.image.blit(self.font.render(line, True, pygame.Color("black")), (5, y))
            for action_button in action_buttons:
                if action_button.button_type is button.ButtonType.MORTGAGE:
                    action_button.update_allow(status.get("allow_mortgage", False))
                elif action_button.button_type is button.ButtonType.UNMORTGAGE:
                    action_button.update_allow(status.get("allow_unmortgage", False))
                elif action_button.button_type is button.ButtonType.ADD_HOUSE:
                    action_button.update_allow(status.get("allow_add_house", False))
                elif action_button.button_type is button.ButtonType.SELL_HOUSE:
                    action_button.update_allow(status.get("allow_sell_house", False))
                self.image.blit(action_button.image, action_button.rect)
        # TODO add these buttons to button spirite in main for detecting buttons

    def _process_property_status(self, property_status: list[dict[str, Any]]) -> None:
        """process property status for display. Sort by property_set_id and then property_id"""

        for status in property_status:
            property_data = data.CONST_PROPERTY_DATA[status["property_id"]]
            status["name"] = property_data["name"]
            status["price"] = property_data["price"]
            status["property_set_id"] = property_data["property_set_id"]
            status["price_of_house"] = property_data.get("price_of_house")
            status["price_of_hotel"] = property_data.get("price_of_hotel")
        property_status.sort(key=lambda x: (x["property_set_id"], x["property_id"]))

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.allow:
            surface.blit(self.image, self.rect)

    def update_allow(self, allow: bool) -> None:
        self.allow = allow

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)

    def _create_property_buttons(
        self, y: int, user_id: str, property_id: int
    ) -> list[button.Button]:
        button_names = ["Mortgage", "Unmortgage", "Add House", "Sell House"]
        buttons_types = [
            button.ButtonType.MORTGAGE,
            button.ButtonType.UNMORTGAGE,
            button.ButtonType.ADD_HOUSE,
            button.ButtonType.SELL_HOUSE,
        ]
        property_buttons: list[button.Button] = []
        START_X = int(0.35 * self.width)
        WIDTH = 70
        HEIGHT = 20
        for i, (name, button_type) in enumerate(zip(button_names, buttons_types)):
            property_buttons.append(
                button.Button(
                    START_X + i * (WIDTH + 10),
                    y,
                    WIDTH,
                    HEIGHT,
                    name,
                    user_id,
                    button_type,
                    property_id,
                    text_size=10,
                )
            )
        return property_buttons
