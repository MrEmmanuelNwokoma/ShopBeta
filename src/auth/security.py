"""Hashing and verfication of password"""
import bcrypt

def hash_password(password: str) -> str:
    """Function for hashing password"""   
    hashed_password =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed_password


def encode_to_bytes(plain_password: str):
    """Function for encoding plain password to bytes """
    plain_bytes = plain_password.encode('utf-8')
    return plain_bytes




def verify_password(plain_password: str, hashed_password: str):
    """function to verifiy password"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """function to verify password"""
#     encoded_password = encode_to_bytes(plain_password)
#     return bcrypt.checkpw(encoded_password, hashed_password)
