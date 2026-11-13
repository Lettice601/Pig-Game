import asyncio
import logging
import websockets

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG level shows detailed logs
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# Optional: limit logs from other libraries if too noisy
logging.getLogger("asyncio").setLevel(logging.WARNING)

async def echo_client():
    uri = "wss://echo.websocket.org"  # Example public echo server
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket!")
        response = await websocket.recv()
        print("Received:", response)

if __name__ == "__main__":
    asyncio.run(echo_client())