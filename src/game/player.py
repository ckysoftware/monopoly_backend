from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from game import card

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from game import space


@dataclass(kw_only=True, slots=True)
class Player:
    name: str
    uid: int  # TODO change to id, unless use uuid
    cash: int
    token: int | None = None
    properties: list[space.Property] = field(default_factory=list)
    position: int = 0
    jail_cards: list[card.ChanceCard] = field(default_factory=list)
    jail_turns: int | None = None

    def __eq__(self, other: object):
        assert isinstance(other, Player)
        return self.uid == other.uid

    def add_property(self, property_: space.Property) -> None:
        self.properties.append(property_)

    def assign_token(self, token: int) -> None:
        self.token = token

    def move(self, position: Optional[int] = None, steps: Optional[int] = None) -> int:
        """Move player either by steps or map position"""
        if position is not None:
            self.position = position
        elif steps is not None:
            self.position += steps
        else:
            raise ValueError("Either steps or position must be provided")
        return self.position

    def offset_position(self, offset: int) -> int:
        # offset position after passing Go
        if self.position < offset:
            return self.position
        else:
            self.position -= offset
            return self.position

    def add_cash(self, amount: int) -> int:
        self.cash += amount
        return self.cash

    def sub_cash(self, amount: int) -> int:
        self.cash -= amount
        return self.cash

    def add_jail_card(self, jail_card: card.ChanceCard) -> None:
        self.jail_cards.append(jail_card)

    # TODO test new parameters
    def use_jail_card(self, card_id: Optional[int] = None) -> card.ChanceCard:
        if len(self.jail_cards) == 0:
            raise ValueError("No jail cards available")
        if card_id is None:
            return self.jail_cards.pop(0)
        else:
            for idx, jail_card in enumerate(self.jail_cards):
                if card_id == jail_card.id:
                    return self.jail_cards.pop(idx)
            raise ValueError(f"Jail card {card_id} not found")

    def get_jail_card_ids(self) -> list[int]:
        return [card.id for card in self.jail_cards]
