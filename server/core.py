import asyncio
from protocol.packet import TFTPPacket
from server.session import TFTPSession
from handlers.rrq import RRQHandler
from handlers.wrq import WRQHandler


class TFTPServerProtocol(asyncio.DatagramProtocol):

    def __init__(self, config):
        self.config = config
        self.handlers = {
            1: RRQHandler(),
            2: WRQHandler()
        }

    def connection_made(self, transport):
        self.transport = transport
        print("Async TFTP Server started")

    def datagram_received(self, data, addr):
        asyncio.create_task(self.handle_request(data, addr))

    async def handle_request(self, data, addr):
        request = TFTPPacket.parse(data)
        opcode = request.get("opcode")

        if opcode not in self.handlers:
            return

        session = TFTPSession(addr, request, self.config)
        handler = self.handlers[opcode]

        await handler.handle(session)