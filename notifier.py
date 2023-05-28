from typing import List

from starlette.websockets import WebSocket


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, uid: str):
        await self.generator.asend(uid)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, uid: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            # customer_by_card = await get_customer_object_by_card_uid(cer_uid=uid) #

            await websocket.send_json({"uid": uid, "is_new_card": False, "payload": None})
            living_connections.append(websocket)
        self.connections = living_connections


notifier = Notifier()
