import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        data = {
            'api_key': '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',
            'model': 'gpt-3.5-turbo',
            'prompt': 'Your prompt here',
            'text': 'Chunk1\n=======\nChunk2\n=======\nChunk3'
        }
        await websocket.send(json.dumps(data))

        while True:
            response = await websocket.recv()
            print(response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
