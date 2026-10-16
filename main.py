import asyncio
import json
from websockets.asyncio.server import serve
from config import *
from cpu import cpu_turn

players = ["Player 1", "Player 2"]
player_scores = [0, 0]
current_player = 0
choose_roll = False


def swap_player():
    global current_player
    if current_player == 0:
        current_player = 1
    else:
        current_player = 0

def play_turn(player_index):
    turn_total = 0
    while True:
        if input(f"{players[player_index]}: (R)oll or (H)old? ").lower() == "r":
            if not DEBUG_ENABLE or not choose_roll:
                roll = roll_dice()
            else:
                roll = input()

            if roll == 1:
                print(f"{players[player_index]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"You rolled a {roll}. Total points this turn: {turn_total}")
        else:
            print(f"{players[player_index]} decides to hold. Total points this turn: {turn_total}")
            return turn_total

async def recv_turn(websocket):
    end_of_turn = False
    turn_total = 0
    while not end_of_turn:
        action = await websocket.recv()
        action = json.loads(action)
        if action["action"] == "r":
            if action["roll"] == 1:
                return 0
            else:
                turn_total += action["roll"]
                print(f"You rolled a {action["roll"]}. Total points this turn: {action["turn_total"]}")
        if action["action"] == "h":
            end_of_turn = True
    return(turn_total)

def main():
    global current_player
    global choose_roll
    if DEBUG_ENABLE and input("Choose roll?").lower == "y":
        choose_roll = True

    cpu_enabled = False
    players[0] = input("Enter name for Player 1: ")
    players[1] = input("Enter name for Player 2: ")
    if input("Do you want to play against the CPU? (y/n): ").lower() == "y":
        cpu_enabled = True

    while max(player_scores) < points_to_win:
        print(f"\n{players[current_player]}'s turn. Current score: {players[0]}: {player_scores[0]}, {players[1]}: {player_scores[1]}.")
        if cpu_enabled:
            if current_player == 1:
                player_scores[1] += cpu_turn(player_scores, players)
                if max(player_scores) < points_to_win:
                    current_player = 0
            else:
                player_scores[0] += play_turn(0)
                if max(player_scores) < points_to_win:
                    current_player = 1
        else:
            player_scores[current_player] += play_turn(current_player)
            swap_player()
    
    if cpu_enabled:
        print(f"{players[current_player]} won!")
    else:
        swap_player()
        print(f"{players[current_player]} won!")

async def online_main_server(websocket):
    global current_player
    players[0] = input("Enter name for Player 1: ")
    players[1] = await websocket.recv()

    while max(player_scores) < points_to_win:
        print(f"\n{players[current_player]}'s turn. Current score: {players[0]}: {player_scores[0]}, {players[1]}: {player_scores[1]}.")

        if current_player == 0:
            player_scores[current_player] += play_turn(current_player)
            swap_player()
        else:
            player_scores[current_player] += recv_turn()
            


while True:
    if input("Would you like to play online? (Y/N)").lower() == "y":
        usr_input = input("(H)ost or input host IP: ").lower
        if usr_input == "h":
            asyncio.run(online_main_server())
        else:
            print("goodbye")
    else:
        main()

    player_scores[0], player_scores[1] = 0, 0
    current_player = 0
    if input("Do you want to play again? (Y/N) ").lower() != "y":
        break