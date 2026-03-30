import socket
from handlers.base import TransferHandler
from protocol.packet import TFTPPacket


class WRQHandler(TransferHandler):

    async def handle(self, session):
        try:
            filepath = session.get_file_path()
        except Exception:
            await session.send_error(2, "Access violation")
            return


        with open(filepath, "wb") as f:
            block = 0
            await session.send(TFTPPacket.ack(block))

            while True:
                try:
                    pkt, raw = await session.receive()
                except socket.timeout:
                    continue

                opcode = int.from_bytes(raw[:2], "big")
                if opcode != 3:
                    continue

                recv_block = int.from_bytes(raw[2:4], "big")
                data = raw[4:]

                if recv_block == block + 1:
                    f.write(data)
                    block += 1

                await session.send(TFTPPacket.ack(block))

                if len(data) < session.config.BLOCK_SIZE:
                    break