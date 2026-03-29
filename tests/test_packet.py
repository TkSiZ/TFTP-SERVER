from protocol.packet import TFTPPacket


def test_ack():
    pkt = TFTPPacket.ack(5)
    parsed = TFTPPacket.parse(pkt)

    assert parsed["opcode"] == 4
    assert parsed["block"] == 5

def test_data():
    pkt = TFTPPacket.data(1, b"hello")
    parsed = TFTPPacket.parse(pkt)

    assert parsed["opcode"] == 3

def test_rrq():
    raw = b"\x00\x01test.txt\x00octet\x00"
    parsed = TFTPPacket.parse(raw)

    assert parsed["opcode"] == 1
    assert parsed["filename"] == "test.txt"