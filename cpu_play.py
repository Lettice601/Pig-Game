from config import *

def cpu_turn():
    turn_total = 0
    while True:
        if player_scores[1] + turn_total <= player_scores[0] + 10:
            roll = roll_dice()
            if roll == 1:
                print(f"{players[1]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"{players[1]} rolled a {roll}. Total points this turn: {turn_total}")

        else:
            print(f"{players[1]} decides to hold. Total points this turn: {turn_total}")
            return turn_total