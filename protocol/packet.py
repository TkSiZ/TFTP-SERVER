class TFTPPacket:

    @staticmethod
    def parse(data: bytes):
        opcode = int.from_bytes(data[:2], "big")

        if opcode in (1, 2):  # RRQ / WRQ
            parts = data[2:].split(b"\x00")
            return {
                "opcode": opcode,
                "filename": parts[0].decode(),
                "mode": parts[1].decode()
            }

        elif opcode == 4:  # ACK
            return {
                "opcode": opcode,
                "block": int.from_bytes(data[2:4], "big")
            }

        return {"opcode": opcode}

    @staticmethod
    def data(block: int, payload: bytes):
        return b"\x00\x03" + block.to_bytes(2, "big") + payload

    @staticmethod
    def ack(block: int):
        return b"\x00\x04" + block.to_bytes(2, "big")

    @staticmethod
    def error(code: int, message: str):
        return b"\x00\x05" + code.to_bytes(2, "big") + message.encode() + b"\x00"