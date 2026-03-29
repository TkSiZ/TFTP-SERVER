import asyncio
import os

from config import TFTPConfig
from server.core import TFTPServerProtocol


async def main():
    os.makedirs(TFTPConfig.BASE_DIR, exist_ok=True)

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TFTPServerProtocol(TFTPConfig),
        local_addr=(TFTPConfig.HOST, TFTPConfig.PORT)
    )

    print(f"TFTP server running on {TFTPConfig.HOST}:{TFTPConfig.PORT}")

    try:
        await asyncio.Future()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())