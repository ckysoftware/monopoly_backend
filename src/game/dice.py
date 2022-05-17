"""
However, if a player rolls Doubles three times in succession (in one turn),
they immediately move to Jail without moving the third time. The only exception
on this is if the player threw 2 doubles,
then hit a nearest utility space from the "Chance" space that is not mortgaged
or unsold, and then the player hits a third pair of doubles,
which would normally send them to jail. However since they only did it for the rent calculation and not movement,
playing continues unless they hit Doubles a fourth time in a row, thus going to jail.
"""

import random


def roll(num_faces: int = 6, num_dice: int = 2) -> tuple[int, ...]:
    return tuple(random.randint(1, num_faces) for _die in range(num_dice))
