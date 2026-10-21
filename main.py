from config import *
import local_play as lp
import online_play_server as ops
import online_play_client as opl

while True:
    if input("Do you want to play online? (Y/N) ").lower != "y":
        lp.local_game()
        if input("Do you want to play again? (Y/N) ").lower() != "y":
            break
    else:
        if input("Host? (Y/N) ").lower != "y":
            ops.main
        else:
            opl.