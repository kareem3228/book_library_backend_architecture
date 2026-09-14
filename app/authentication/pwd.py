import bcrypt


def hash_password(password:str):
    password_byte=password.encode("utf-8")
    salt=bcrypt.gensalt()
    passwordhash=bcrypt.hashpw(
        salt=salt,
        password=password_byte
    )
    return passwordhash.decode("utf-8")

def verify_password(Password:str,stored_password:str):
    password_byte=Password.encode("utf-8")
    hashed_password_byte=stored_password.encode("utf-8")
    result=    bcrypt.checkpw(
            password=password_byte,
            hashed_password=hashed_password_byte
        )
    return result