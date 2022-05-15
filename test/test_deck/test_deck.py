import pytest
from game import card


def test_deck_init_from_data_and_cards(chance_cards_deck, chance_cards_full):
    init_from_card = card.Deck(name="Chance Cards")
    init_from_card.shuffle_add_cards(cards=chance_cards_full, seed=9001)
    assert init_from_card.name == chance_cards_deck.name
    assert init_from_card.cards == chance_cards_deck.cards


def test_deck_draw_unownable(chance_cards_deck):
    chance_cards_deck.cards[0].ownable = False
    original_card = chance_cards_deck.cards[0]
    original_length = len(chance_cards_deck.cards)

    drawn_card = chance_cards_deck.draw_card()
    assert drawn_card == original_card

    assert len(chance_cards_deck.cards) == original_length
    assert drawn_card == chance_cards_deck.cards[-1]


def test_deck_incorrect_shuffle_add():
    deck = card.Deck(name="Incorrect shuffle add")
    with pytest.raises(ValueError, match="Either cards or data must be provided"):
        deck.shuffle_add_cards(cards=None, data=None, seed=None)


def test_deck_draw_ownable(chance_cards_deck):
    chance_cards_deck.cards[0].ownable = True
    original_card = chance_cards_deck.cards[0]
    original_length = len(chance_cards_deck.cards)

    drawn_card = chance_cards_deck.draw_card()
    assert drawn_card == original_card

    assert len(chance_cards_deck.cards) == original_length - 1
    assert drawn_card != chance_cards_deck.cards[-1]


def test_deck_append_owned_card(chance_cards_deck):
    chance_cards_deck.cards[0].ownable = True
    original_length = len(chance_cards_deck.cards)

    drawn_card = chance_cards_deck.draw_card()
    chance_cards_deck.append_owned_card(card=drawn_card)

    assert len(chance_cards_deck.cards) == original_length
    assert chance_cards_deck.cards[-1] == drawn_card
