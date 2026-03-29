from protocol.packet import TFTPPacket
from server.retransmit import RetransmissionManager


class RRQHandler:

    async def handle(self, session):
        try:
            filepath = session.get_file_path()
        except Exception:
            await session.send_error(2, "Access violation")
            return

        try:
            f = open(filepath, "rb")
        except FileNotFoundError:
            await session.send_error(1, "File not found")
            return

        retransmit = RetransmissionManager(
            session.config.MAX_RETRIES,
            session.config.TIMEOUT
        )

        block = 1

        while True:
            chunk = f.read(session.config.BLOCK_SIZE)

            async def send():
                await session.send(TFTPPacket.data(block, chunk))

            async def wait_ack():
                pkt, _ = await session.receive()
                return pkt

            success = await retransmit.run(
                send,
                wait_ack,
                lambda pkt: pkt["opcode"] == 4 and pkt["block"] == block
            )

            if not success:
                return

            if len(chunk) < session.config.BLOCK_SIZE:
                break

            block += 1