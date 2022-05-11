import random
from collections import deque
from dataclasses import dataclass

from .chance_card import ChanceCard


# TODO write test
@dataclass(kw_only=True, slots=True)
class Deck:
    """
    Class containing a set of chance cards / community chest cards
    """

    name: str  # chance card or community chest
    cards: deque[ChanceCard] = None

    def shuffle_add_cards(
        self, cards: list[ChanceCard] = None, data: list[dict] = None, seed: int = None
    ) -> None:
        """
        Add the cards after shuffling. This should be called before using the deck and after initialization.

        cards: A List of ChanceCard. Either cards or data must be provided.
        data: A List of dict containging data to initialize ChanceCard. Either cards or data must be provided.
        """
        if cards is not None:
            shuffled_cards = random.Random(seed).shuffle(cards)
        elif data is not None:
            initialized_cards = [ChanceCard(**datum) for datum in data]
            shuffled_cards = random.Random(seed).shuffle(initialized_cards)
        else:
            raise ValueError("Either cards or data must be provided.")

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
