import constants as c
import host
import pytest
from game import card, data, space
from game.actions import Action
from game.game import Game
from game.game_map import GameMap
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
def game_map_simple() -> GameMap:
    property_set = space.PropertySet(id=0)
    property_space_1 = space.PropertySpace(
        name="Property 1",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=1,
    )
    property_space_2 = space.PropertySpace(
        name="Property 2",
        price=60,
        rent=[2, 10, 30, 90, 160, 250],
        price_of_house=50,
        price_of_hotel=50,
        HOUSE_LIMIT=c.CONST_HOUSE_LIMIT,
        HOTEL_LIMIT=c.CONST_HOTEL_LIMIT,
        property_set=property_set,
        owner_uid=10,
    )
    property_set.add_property(property_space_1)
    property_set.add_property(property_space_2)
    game_map = GameMap(map_list=[property_space_1, property_space_2])
    return game_map


@pytest.fixture
def game_init(game_map_simple: GameMap) -> Game:
    game = Game()
    game.game_map = game_map_simple
    return game


@pytest.fixture
def game_with_players(game_init: Game) -> Game:
    for i in range(4):
        new_player = Player(name=f"Player {i + 1}", uid=i, cash=c.CONST_STARTING_CASH)
        game_init.players.append(new_player)
    return game_init


@pytest.fixture
def game_beginning(game_with_players: Game) -> Game:
    game_with_players.initialize_first_player()
    game_with_players.initialize()
    return game_with_players


@pytest.fixture
def game_middle(game_beginning: Game) -> Game:
    for player in game_beginning.players:
        player.position = player.uid + 5
        player.cash += player.position * 10 * (-1) ** player.uid

    monopoly_properties = [
        game_beginning.game_map.map_list[1],
        game_beginning.game_map.map_list[3],
    ]
    assert isinstance(monopoly_properties[0], space.PropertySpace)
    assert isinstance(monopoly_properties[1], space.PropertySpace)
    game_beginning.players[1].add_property(monopoly_properties[0])
    game_beginning.players[1].add_property(monopoly_properties[1])
    monopoly_properties[0].assign_owner(1)
    monopoly_properties[1].assign_owner(1)

    monopoly_properties[0].no_of_houses = 4
    monopoly_properties[1].no_of_hotels = 1

    return game_beginning


@pytest.fixture
def fake_jail_card() -> card.ChanceCard:
    return card.ChanceCard(
        id=1,
        description="pytest Fake Jail Card",
        action=Action.COLLECT_JAIL_CARD,
        ownable=True,
    )


@pytest.fixture
def users_simple() -> list[host.User]:
    return [host.User(name=f"User {i + 1}", room_uid="9001") for i in range(4)]


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
