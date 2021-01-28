import asyncio
import json
import websockets


class RemoteSound:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


    async def send(self, data):
        uri = f"ws://{self.ip}:{self.port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(data)


    def send_note(self, note):
        data = json.dumps(note)
        asyncio.get_event_loop().run_until_complete(self.send(data))
