import bcrypt


def salty_password(password: str):
    salt = bcrypt.gensalt()
    return salt.decode(), bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()


def check_same_password(password, hash_password):
    return bcrypt.checkpw(password.encode(), hash_password.encode())
