from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os
load_dotenv()
secret_key= os.getenv('SECRET_KEY')
algorithm='HS256'
def create_access_token(user_id:int):
    expires=datetime.now(timezone.utc)+timedelta(minutes=30)
    payload={
        "sub":str(user_id),
        "exp":expires
    }
    token=jwt.encode(
        claims=payload,
        key=secret_key,
        algorithm=algorithm
    )
    return token
def verify_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            secret_key
            ,algorithms=[algorithm]
        )
        return payload
    except JWTError:
        return None

