import pytest
from game import card, data


@pytest.fixture
def chance_cards_full():
    data_chance_cards = data.CONST_CHANCE_CARDS
    chance_cards = [card.ChanceCard(**datum) for datum in data_chance_cards]
    return chance_cards


@pytest.fixture
def cc_cards_full():
    data_cc_cards = data.CONST_CC_CARDS
    cc_cards = [card.ChanceCard(**datum) for datum in data_cc_cards]
    return cc_cards


@pytest.fixture
def chance_cards_deck():
    chance_card_deck = card.Deck(name="Chance Cards")
    chance_card_deck.shuffle_add_cards(data=data.CONST_CHANCE_CARDS, seed=9001)
    return chance_card_deck


@pytest.fixture
def cc_cards_deck():
    cc_card_deck = card.Deck(name="Community Chest Cards")
    cc_card_deck.shuffle_add_cards(data=data.CONST_CC_CARDS, seed=9001)
    return cc_card_deck
