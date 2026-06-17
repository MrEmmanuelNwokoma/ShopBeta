"""Hashing and verfication of password"""
import bcrypt

def hash_password(password: str) -> str:
    """Function for hashing password"""   
    hashed_password =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed_password



def verify_password(plain_password: str, hashed_password: str):
    """function to verifiy password"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


