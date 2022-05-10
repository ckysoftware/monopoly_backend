import random
from collections import deque
from dataclasses import dataclass, field

from game.card.chance_card import ChanceCard


# TODO write test
@dataclass(kw_only=True, slots=True)
class Deck:
    name: str  # chance card or community chest
    cards: deque[ChanceCard] = field(default_factory=deque)

    def shuffle_add_cards(self, cards: list[ChanceCard], seed: int = None) -> None:
        shuffled_cards = random.Random(seed).shuffle(cards)
        self.cards = deque(shuffled_cards)

    def append_owned_card(self, card: ChanceCard) -> None:
        """
        After a player played his/her owned card, append it to the deck
        """
        self.cards.append(card)

    def draw_card(self) -> ChanceCard:
        drawn_card = self.cards.popleft()

        if drawn_card.ownable is False:  # append the card to the end if not ownable
            self.cards.append(drawn_card)
        return drawn_card  # return for the frontend
