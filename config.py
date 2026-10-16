from random import randint

#------CONFIG OPTIONS------#
DEBUG_ENABLE = 0
points_to_win = 100
dice_size = 6

def roll_dice():
    return randint(1, dice_size)
