from typing import Optional


class GameError(Exception):
    pass


class InvalidActionError(GameError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Game invalid command exception"
        super().__init__(message)


class InsufficientCashError(InvalidActionError):
    def __init__(self, player_id: int, cur_amount: int, req_amount: int):
        message = f"""Player {player_id} does not have enough cash to pay {req_amount}
         (current amount: {cur_amount}, difference: {req_amount - cur_amount})"""
        self.player_id = player_id
        self.cur_amount = cur_amount
        self.req_amount = req_amount
        super().__init__(message)
