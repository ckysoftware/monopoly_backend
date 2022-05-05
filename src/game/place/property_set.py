from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from src.game.place.property import Property


@dataclass(kw_only=True)
class PropertySet:
    set_id: int
    properties: list[Property] = field(default_factory=list)
    monopoly: bool = False

    def add_property(self, property: Property) -> None:
        self.properties.append(property)

    def update_monopoly(self):
        if len(self.properties) == 0:
            self.monopoly = False
            return

        owner_character = self.properties[0].owner_character
        for property in self.properties[1:]:
            if property.owner_character != owner_character:
                self.monopoly = False
                return
        self.monopoly = True

    def count_owned(self, owner_character: int):
        """
        Return the number of properties owned by this owner
        """
        count = 0
        for property in self.properties:
            if property.owner_character == owner_character:
                count += 1
        return count
