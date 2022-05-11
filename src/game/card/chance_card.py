from dataclasses import dataclass

from game.actions import Action


# TODO write test
@dataclass(kw_only=True, slots=True)
class ChanceCard:
    """
    class for both chance card and community chest card
    """

    card_id: int
    description: str
    action: Action
    ownable: bool  # whether this card can be kept by the player

    def trigger(self) -> Action:
        return self.action
