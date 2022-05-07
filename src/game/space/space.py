from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.actions import Action as A
    from game.player import Player


@dataclass(kw_only=True, slots=True)
class Space(ABC):
    name: str

    @abstractmethod
    def trigger(self, player: Player) -> A:
        """
        This method triggers the card's action and return action result.
        """
        pass
