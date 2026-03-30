def parse_options(parts):
    options = {}

    for i in range(2, len(parts) - 1, 2):
        key = parts[i].decode().lower()
        value = parts[i + 1].decode()
        options[key] = value

    return options


def build_oack(options: dict):
    payload = b""

    for k, v in options.items():
        payload += k.encode() + b"\x00" + str(v).encode() + b"\x00"

    return b"\x00\x06" + payload