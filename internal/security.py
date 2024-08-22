import bcrypt


def hash_password(password: str):
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash
    

def check_password(password: str, hash: str):
    userBytes = password.encode('utf-8')
    # checking password
    result = bcrypt.checkpw(userBytes, hash)
    return result
