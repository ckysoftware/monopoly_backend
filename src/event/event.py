import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


class EventType(enum.Enum):
    G_DICE_ROLL = "g_dice_roll"
    G_MOVE = "g_move"
    G_CASH_CHANGE = "g_cash_change"
    G_ADD_PLAYER = "g_add_player"
    G_ALL_STATES = "g_all_states"
    G_CURRENT_PLAYER = "g_current_player"
    G_WAIT_FOR_ROLL = "g_wait_for_roll"
    G_WAIT_FOR_END_TURN = "g_wait_for_end_turn"
    G_ASK_TO_BUY = "g_ask_to_buy"
    G_BUY_PROPERTY = "g_buy_property"

    V_ADD_PLAYER = "v_add_player"
    V_ROLL_AND_MOVE = "v_roll_and_move"
    V_ASSIGN_TOKEN = "v_assign_token"
    V_START_GAME = "v_start_game"
    V_END_TURN = "v_end_turn"
    V_BUY_PROPERTY = "v_buy_property"


@dataclass(slots=True)
class Event:
    """Base class for all events"""

    event_type: EventType
    message: dict[str, Any]
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = field(default_factory=datetime.utcnow)


# @dataclass(slots=True)
# class DiceRolled:
#     """Event that is published when dice are rolled"""

#     dice_1: int
#     dice_2: int

#     def __init__(self, dice_1: int, dice_2: int) -> None:
#         self.dice_1 = dice_1
#         self.dice_2 = dice_2
