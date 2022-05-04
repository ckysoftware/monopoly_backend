from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from property_card import PropertyCard


@dataclass(kw_only=True)
class PropertySet:
    set_id: int
    properties: list[PropertyCard] = field(default_factory=list)
    monopoly: bool = False

    def add_property(self, property_card: PropertyCard) -> None:
        self.properties.append(property_card)

    def update_monopoly(self):
        if len(self.properties) == 0:
            self.monopoly = False
            return

        owner_character = self.properties[0].owner_character
        for property_card in self.properties[1:]:
            if property_card.owner_character != owner_character:
                self.monopoly = False
                return
        self.monopoly = True
