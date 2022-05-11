from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game.actions import Action
    from game.player import Player


@dataclass(kw_only=True, slots=True)
class Space(ABC):
    name: str

    @abstractmethod
    def trigger(self, player: Player) -> Action:
        """
        This method triggers the space's action and return action result.
        """
        pass
