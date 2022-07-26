from dataclasses import dataclass

import model


@dataclass(kw_only=True, slots=True)
class GameController:
    # token_view: view.PlayerToken
    game_model: model.GameModel

    def roll_dice(self):
        ...

    def move_player(self, position: int):
        ...
