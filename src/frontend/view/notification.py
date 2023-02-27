from typing import Any

import pygame


class Notification(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 12)

        self.texts = [self.font.render("", True, pygame.Color("black"))]
        self.allow: bool = True
        self.rect: pygame.rect.Rect = pygame.Rect(x, y, width, height)
        self.image: pygame.surface.Surface
        self.update()

    def update(self, texts: list[str] = [""], *args: Any, **kwargs: Any) -> None:
        self.image: pygame.surface.Surface = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))

        self.texts = [
            self.font.render(line, True, pygame.Color("black"))
            for text in texts
            for line in self._wrap_text(text)
        ]
        for i, text in enumerate(self.texts):
            self.image.blit(text, (5, i * 20))

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.allow:
            surface.blit(self.image, self.rect)

    def update_allow(self, allow: bool) -> None:
        self.allow = allow

    def update_rect(self, x: int, y: int) -> None:
        self.rect.center = (x, y)

    @staticmethod
    def _wrap_text(text: str, width: int = 45) -> list[str]:
        """wrap text to fit in notification box.
        Text in a line longer than the width will be put into another str.
        """
        if len(text) <= width:
            return [text]
        else:
            lines: list[str] = []
            line: list[str] = []
            cur_line_width = 0
            for word in text.split():
                if cur_line_width + len(word) <= width:
                    line.append(word)
                    cur_line_width += len(word) + 1  # +1 for space
                else:
                    lines.append(" ".join(line))
                    line = [word]
                    cur_line_width = len(word) + 1  # +1 for space
            lines.append(" ".join(line))
            return lines
