import game.dice as dice


def test_roll_two_dice():
    for _ in range(100):
        dice_1, dice_2 = dice.roll(num_faces=6, num_dice=2)
        assert dice_1 in list(range(1, 7))
        assert dice_2 in list(range(1, 7))


def test_roll_three_dice():
    for _ in range(100):
        dice_1, dice_2, dice_3 = dice.roll(num_faces=6, num_dice=3)
        assert dice_1 in list(range(1, 7))
        assert dice_2 in list(range(1, 7))
        assert dice_3 in list(range(1, 7))
