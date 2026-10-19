#!/usr/bin/env python

from websockets.sync.client import connect

def main():
    uri = "ws://localhost:8765"
    with connect(uri) as websocket:
        while True:
            msg = input("message to send")

            websocket.send(msg)
            print(f">>> {msg}")

            recvd_msg = websocket.recv()
            print(f"<<< {recvd_msg}")

if __name__ == "__main__":
    main()