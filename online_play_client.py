from websockets.sync.client import connect
from config import *
import asyncio
import json

players = ["Player 1", "Player 2"]
player_scores = [0, 0]
current_player = 0

async def play_turn(websocket):
    turn_total = 0
    while True:
        if input(f"{players[1]}: (R)oll or (H)old? ").lower() == "r":
            roll = roll_dice()
            websocket.send(json.dumps({"action": "r", "roll": roll}))
            if roll == 1:
                print(f"{players[1]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"You rolled a {roll}. Total points this turn: {turn_total}")
        else:
            websocket.send(json.dumps({"action": "h", "roll": 0}))
            print(f"{players[1]} decides to hold. Total points this turn: {turn_total}")
            return turn_total

async def recv_turn(websocket):
    turn_total = 0

    while True:
        action = websocket.recv()
        action = json.loads(action)

        if action["action"] == "r":
            if action["roll"] == 1:
                print(f"{players[0]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += action["roll"]
                print(f"{players[0]} rolled a {action['roll']}. Total points this turn: {turn_total}")
        else:
            print(f"{players[0]} decides to hold. Total points this turn: {turn_total}")
            return turn_total


async def connect_to_server(websocket):
    player_scores = [0, 0]
    current_player = 0

    settings = websocket.recv()
    settings = json.loads(settings)
    points_to_win: int = settings["points_to_win"]
    dice_size: int = settings["dice_size"]
    players[0] = settings["p1_name"]
    print(f"Player 1's name is {players[0]}")

    players[1] = input("Player 2 name: ")
    websocket.send(json.dumps({"p2_name": players[1]}))

    while max(player_scores) < points_to_win:
        print(f"\n{players[current_player]}'s turn. Current score: {players[0]}: {player_scores[0]}, {players[1]}: {player_scores[1]}.")
        if current_player == 1:
            player_scores[1] += await play_turn(websocket)
            current_player = 0

        elif current_player == 0:
            player_scores[0] += await recv_turn(websocket)
            current_player = 1

    if current_player == 0:
        print(f"{players[1]} won!")
    elif current_player == 1:
        print(f"{players[0]} won!")
    else:
        raise ValueError("Error: Invalid current_player value.")

if __name__ == "__main__":
    uri = "ws://localhost:8765"
    with connect(uri) as websocket:
        while True:
            asyncio.run(connect_to_server(websocket))