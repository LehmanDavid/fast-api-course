from jose import JWTError, jwt
from datetime import datetime, timedelta
#SECRET_KEY
#Algorithm
#Exporation time

SECRET_KEY = 'a3344cd21c53ce65bcfa03fbb46e75e1d19e7b44211a1434a07d3a034d32e164'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt