from config import *
import local_play as lp

while True:
    lp.local_game()
    if input("Do you want to play again? (Y/N) ").lower() != "y":
        break