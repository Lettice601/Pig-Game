from config import *
import random as r
from time import sleep


def compute_chance_to_hold(turn_total):
    return(1-((25-turn_total)/25))

def cpu_turn(player_scores, players):
    turn_total = 0
    while True:
        if DEBUG_ENABLE:
            print(compute_chance_to_hold(turn_total))
        if r.random() >= compute_chance_to_hold(turn_total):
            roll = roll_dice()
            if roll == 1:
                print(f"{players[1]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"{players[1]} rolled a {roll}. Total points this turn: {turn_total}") 
                sleep(1)

        else:
            print(f"{players[1]} decides to hold. Total points this turn: {turn_total}")
            return(turn_total)