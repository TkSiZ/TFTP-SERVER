import asyncio
import socket
from protocol.packet import TFTPPacket


import os

class TFTPSession:

    def __init__(self, client_addr, request, config):
        self.client_addr = client_addr
        self.request = request
        self.config = config

        self.loop = asyncio.get_event_loop()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

    async def send(self, data: bytes):
        await self.loop.sock_sendto(self.sock, data, self.client_addr)

    async def receive(self):
        data, _ = await self.loop.sock_recvfrom(self.sock, 2048)
        return TFTPPacket.parse(data), data

    async def send_error(self, code, message):
        await self.send(TFTPPacket.error(code, message))

    def get_file_path(self):
        base = os.path.abspath(self.config.BASE_DIR)

        filename = os.path.normpath(self.request["filename"])
        full_path = os.path.abspath(os.path.join(base, filename))

        if not full_path.startswith(base):
            raise Exception("Access violation")

        return full_path