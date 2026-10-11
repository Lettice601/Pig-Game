#------CONFIG OPTIONS------#
points_to_win = 100
dice_size = 6
players = ["Player 1", "Player 2"]
player_scores = [0, 0]
current_player = 0

#------HELPER FUNCTIONS------#
from random import randint

def roll_dice():
    return randint(1, dice_size)