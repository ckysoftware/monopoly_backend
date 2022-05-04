from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.player import Player


@dataclass
class Place(ABC):
    name: str

    @abstractmethod
    def trigger(self, player: Player) -> int:
        """
        This method triggers the card's action and return action result.
        """
        pass
