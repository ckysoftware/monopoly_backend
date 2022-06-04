import constants as c
import pytest
from game import card, data
from game.player import Player


@pytest.fixture
def chance_cards_full() -> list[card.ChanceCard]:
    data_chance_cards = data.CONST_CHANCE_CARDS
    chance_cards = [card.ChanceCard(**datum) for datum in data_chance_cards]
    return chance_cards


@pytest.fixture
def cc_cards_full() -> list[card.ChanceCard]:
    data_cc_cards = data.CONST_CC_CARDS
    cc_cards = [card.ChanceCard(**datum) for datum in data_cc_cards]
    return cc_cards


@pytest.fixture
def chance_cards_deck() -> card.Deck:
    chance_card_deck = card.Deck(name="Chance Cards")
    chance_card_deck.shuffle_add_cards(data=data.CONST_CHANCE_CARDS, seed=9001)
    return chance_card_deck


@pytest.fixture
def cc_cards_deck() -> card.Deck:
    cc_card_deck = card.Deck(name="Community Chest Cards")
    cc_card_deck.shuffle_add_cards(data=data.CONST_CC_CARDS, seed=9001)
    return cc_card_deck


@pytest.fixture
def player_simple() -> Player:
    player = Player(name="Player 1", uid=0, cash=c.CONST_STARTING_CASH)
    return player


@pytest.fixture
def map_list() -> list[str]:
    map_names: list[str] = [
        "Go",
        "Mediterranean Avenue",
        "Community Chest",
        "Baltic Avenue",
        "Income Tax",
        "Reading Railroad",
        "Oriental Avenue",
        "Chance",
        "Vermont Avenue",
        "Connecticut Avenue",
        "Jail",
        "St. Charles Place",
        "Electric Company",
        "States Avenue",
        "Virginia Avenue",
        "Pennsylvania Railroad",
        "St. James Place",
        "Community Chest",
        "Tennessee Avenue",
        "New York Avenue",
        "Free Parking",
        "Kentucky Avenue",
        "Chance",
        "Indiana Avenue",
        "Illinois Avenue",
        "B. & O. Railroad",
        "Atlantic Avenue",
        "Ventnor Avenue",
        "Water Works",
        "Marvin Gardens",
        "Go To Jail",
        "Pacific Avenue",
        "North Carolina Avenue",
        "Community Chest",
        "Pennsylvania Avenue",
        "Short Line",
        "Chance",
        "Park Place",
        "Luxury Tax",
        "Boardwalk",
    ]
    return map_names


@pytest.fixture
def chance_card_list() -> set[int]:
    chance_cards: set[int] = set([datum["id"] for datum in data.CONST_CHANCE_CARDS])
    return chance_cards


@pytest.fixture
def cc_card_list() -> set[int]:
    cc_cards: set[int] = set([datum["id"] for datum in data.CONST_CC_CARDS])
    return cc_cards
