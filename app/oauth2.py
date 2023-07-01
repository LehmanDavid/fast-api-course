from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from . import models


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY
# Algorithm
# Exporation time

SECRET_KEY = 'a3344cd21c53ce65bcfa03fbb46e75e1d19e7b44211a1434a07d3a034d32e164'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data  # user_id


def get_current_user(token: schemas.TokenData = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentionals_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credentionals_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
