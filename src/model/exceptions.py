from typing import Optional


class CommandError(Exception):
    pass


class GameInvalidCommandError(CommandError):
    """Exception for all game-related command errors"""

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Game invalid command exception"
        super().__init__(message)


class NotCurrentPlayerError(GameInvalidCommandError):
    """The player sending the command is not the current player"""

    def __init__(self, player_id: int):
        message = f"Player id: {player_id} is not the current player"
        super().__init__(message)


class CommandNotMatchingStateError(GameInvalidCommandError):
    """The command sent does not match the current game state"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message)
