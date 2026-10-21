#!/usr/bin/env python

from websockets.sync.client import connect
import aioconsole as aio
import asyncio

async def recv_data(websocket):
    print(f"<<< {await websocket.recv()}")

async def send_data(websocket):
    line = await aio.ainput("Enter Message: ")
    await websocket.send(line)

async def main():
    uri = "ws://localhost:8765"
    with connect(uri) as websocket:
        while True:
            await asyncio.gather(send_data(websocket), recv_data(websocket))

if __name__ == "__main__":
    asyncio.run(main())