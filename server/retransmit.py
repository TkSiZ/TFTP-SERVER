import asyncio


class RetransmissionManager:

    def __init__(self, retries, timeout):
        self.retries = retries
        self.timeout = timeout

    async def run(self, send_func, wait_ack_func, validate):
        for _ in range(self.retries):
            await send_func()

            try:
                pkt = await asyncio.wait_for(wait_ack_func(), timeout=self.timeout)
                if validate(pkt):
                    return True
            except asyncio.TimeoutError:
                continue

        return False