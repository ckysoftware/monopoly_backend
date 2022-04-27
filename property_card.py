from dataclasses import dataclass

from card import Card

@dataclass(kw_only=True)
class PropertyCard(Card):
    pass