from random import randint

#------CONFIG OPTIONS------#
DEBUG_ENABLE = 1
points_to_win = 100
dice_size = 6

def roll_dice():
    return randint(1, dice_size)

def min_max_scale(val, min_val, max_val):
    # Avoid DivisionByZero if all values are identical
    if max_val == min_val:
        return 0.0
    return (val - min_val) / (max_val - min_val)
