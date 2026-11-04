#!/usr/bin/env python

from random import randint

#------CONFIG OPTIONS------#
DEBUG_ENABLE: bool = True
points_to_win: int = 100
dice_size: int = 6

def roll_dice():
    return randint(1, dice_size)
