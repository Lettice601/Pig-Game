from config import *
import random as r
from time import sleep


def compute_chance_to_hold(turn_total, player_scores):
    chance_to_hold = 1-((25-turn_total)/25)
    if DEBUG_ENABLE:
        print(f"Score diff: {(player_scores[0] - turn_total) - player_scores[1]}")
        print(chance_to_hold)
    
    if (player_scores[0] - turn_total) - player_scores[1] > 20:
        chance_to_hold *= max((1 + turn_total - (player_scores[0]))/(turn_total + 1), 0.2)
    
    if DEBUG_ENABLE:
        print(chance_to_hold)
    return(chance_to_hold)

def cpu_turn(player_scores, players):
    turn_total = 0
    while True:
        if r.random() >= compute_chance_to_hold(turn_total, player_scores):
            roll = roll_dice()
            if roll == 1:
                print(f"{players[1]} rolled a 1! No points this turn.")
                return(0)
            else:
                turn_total += roll
                print(f"{players[1]} rolled a {roll}. Total points this turn: {turn_total}") 
                sleep(1)

        else:
            print(f"{players[1]} decides to hold. Total points this turn: {turn_total}")
            return(turn_total)