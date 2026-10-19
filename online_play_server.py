#!/usr/bin/env python

import asyncio
from config import *
import json
from websockets.asyncio.server import serve

players = ["Player 1", "Player 2"]
player_scores = [0, 0]
current_player = 0

async def play_turn(websocket):
    turn_total = 0
    while True:
        if input(f"{players[0]}: (R)oll or (H)old? ").lower() == "r":
            roll = roll_dice()
            websocket.send(json.dumps({"action": "r", "roll": roll}))
            if roll == 1:
                print(f"{players[0]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += roll
                print(f"You rolled a {roll}. Total points this turn: {turn_total}")
        else:
            websocket.send(json.dumps({"action": "h", "roll": 0}))
            print(f"{players[0]} decides to hold. Total points this turn: {turn_total}")
            return turn_total

async def recv_turn(websocket):
    while True:
        action = await websocket.recv()
        action = json.loads(action)

        if action["action"] == "r":
            if action["roll"] == 1:
                print(f"{players[1]} rolled a 1! No points this turn.")
                return 0
            else:
                turn_total += action["roll"]
                print(f"{players[1]} rolled a {action['roll']}. Total points this turn: {turn_total}")
        else:
            print(f"{players[1]} decides to hold. Total points this turn: {turn_total}")
            return turn_total

async def host_server(websocket):
    player_scores = [0, 0]
    current_player = 0
    
    players[0] = input("Player 1 name: ")
    players[1] = await websocket.recv()
    websocket.send("name")
    print(f"Player 2's name is {players[1]}")


    while max(player_scores) < points_to_win:
        print(f"\n{players[current_player]}'s turn. Current score: {players[0]}: {player_scores[0]}, {players[1]}: {player_scores[1]}.")
        if current_player == 0:
            print(await play_turn(websocket))
            player_scores[0] += await play_turn(websocket)
            current_player = 1

        elif current_player == 1:
            player_scores[1] += await recv_turn(websocket)
            current_player = 0


    print(f"{players[current_player]} won!")

async def main():
    server = await serve(host_server, "localhost", 8765)
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())