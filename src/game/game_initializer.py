from game import data, enum_types, game_map, space


def build_game_map(HOUSE_LIMIT: int, HOTEL_LIMIT: int) -> game_map.GameMap:
    property_spaces = _build_property_spaces(
        HOUSE_LIMIT=HOUSE_LIMIT, HOTEL_LIMIT=HOTEL_LIMIT
    )
    railroad_spaces = _build_railroad_spaces()
    utility_spaces = _build_utility_spaces()

    spaces: list[space.Space] = []

    # S
    spaces.append(space.NthSpace(name="Go"))
    spaces.append(property_spaces.pop(0))
    spaces.append(
        space.DrawSpace(name="Community Chest", deck_type=enum_types.DeckType.CC)
    )
    spaces.append(property_spaces.pop(0))
    spaces.append(space.TaxSpace(name="Income Tax", tax_type=enum_types.TaxType.INCOME))
    spaces.append(railroad_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(space.DrawSpace(name="Chance", deck_type=enum_types.DeckType.CHANCE))
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))

    # W
    spaces.append(space.NthSpace(name="Jail"))
    spaces.append(property_spaces.pop(0))
    spaces.append(utility_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(railroad_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(
        space.DrawSpace(name="Community Chest", deck_type=enum_types.DeckType.CC)
    )
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))

    # N
    spaces.append(space.NthSpace(name="Free Parking"))
    spaces.append(property_spaces.pop(0))
    spaces.append(space.DrawSpace(name="Chance", deck_type=enum_types.DeckType.CHANCE))
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(railroad_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(utility_spaces.pop(0))
    spaces.append(property_spaces.pop(0))

    # E
    spaces.append(space.JailSpace(name="Go To Jail"))
    spaces.append(property_spaces.pop(0))
    spaces.append(property_spaces.pop(0))
    spaces.append(
        space.DrawSpace(name="Community Chest", deck_type=enum_types.DeckType.CC)
    )
    spaces.append(property_spaces.pop(0))
    spaces.append(railroad_spaces.pop(0))
    spaces.append(space.DrawSpace(name="Chance", deck_type=enum_types.DeckType.CHANCE))
    spaces.append(property_spaces.pop(0))
    spaces.append(space.TaxSpace(name="Luxury Tax", tax_type=enum_types.TaxType.LUXURY))
    spaces.append(property_spaces.pop(0))
    #######

    assert len(spaces) == 40
    assert len(property_spaces) == 0
    assert len(railroad_spaces) == 0
    assert len(utility_spaces) == 0

    map_ = game_map.GameMap(map_list=spaces)

    return map_


def _build_property_spaces(
    HOUSE_LIMIT: int, HOTEL_LIMIT: int
) -> list[space.PropertySpace]:
    property_sets: dict[int, space.PropertySet] = {}  # id, PropertySet
    property_spaces: list[space.PropertySpace] = []
    for property_data in data.CONST_PROPERTY_SPACES:
        property_set_id = property_data["property_set_id"]
        if property_set_id not in property_sets:  # new property set
            property_sets[property_set_id] = space.PropertySet(id=property_set_id)
        new_property_space = space.PropertySpace(
            name=property_data["name"],
            price=property_data["price"],
            rent=property_data["rent"],
            price_of_house=property_data["price_of_house"],
            price_of_hotel=property_data["price_of_hotel"],
            property_set=property_sets[property_set_id],
            HOUSE_LIMIT=HOUSE_LIMIT,
            HOTEL_LIMIT=HOTEL_LIMIT,
        )
        property_sets[property_set_id].add_property(new_property_space)
        property_spaces.append(new_property_space)
    return property_spaces


def _build_railroad_spaces() -> list[space.RailroadSpace]:
    property_set = space.PropertySet(
        id=data.CONST_RAILROAD_SPACES[0]["property_set_id"]
    )
    railroad_spaces: list[space.RailroadSpace] = []
    for railroad_data in data.CONST_RAILROAD_SPACES:
        new_railroad_space = space.RailroadSpace(
            name=railroad_data["name"],
            price=railroad_data["price"],
            rent=railroad_data["rent"],
            property_set=property_set,
        )
        property_set.add_property(new_railroad_space)
        railroad_spaces.append(new_railroad_space)
    return railroad_spaces


def _build_utility_spaces() -> list[space.UtilitySpace]:
    property_set = space.PropertySet(id=data.CONST_UTILITY_SPACES[0]["property_set_id"])
    utility_spaces: list[space.UtilitySpace] = []
    for utility_data in data.CONST_UTILITY_SPACES:
        new_utility_space = space.UtilitySpace(
            name=utility_data["name"],
            price=utility_data["price"],
            property_set=property_set,
        )
        property_set.add_property(new_utility_space)
        utility_spaces.append(new_utility_space)
    return utility_spaces
