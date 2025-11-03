import secrets


def generate_random_code_128() -> int:
    return secrets.randbits(128)

