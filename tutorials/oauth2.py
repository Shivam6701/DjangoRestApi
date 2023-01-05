from rest_framework import exceptions
from telnetlib import STATUS
from wsgiref import headers
from jose import JWTError,jwt
from datetime import datetime, timedelta
from rest_framework import status
from . import schemas
from tutorials.models import User
from tutorials.serializers import UserSerializer
#Secret key
#algoritm
#expiration time

SECRET_KEY= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_INUTES= 30

def create_access_token(data: dict):
    to_encode =data.copy()

    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_INUTES)
    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(request):
    bearer = request.headers['Authorization']
    token = bearer.split()[1]
    credentials_exception= exceptions.AuthenticationFailed
    token_id=verify_access_token(token, credentials_exception)
    try:
        user= User.objects.get(pk=token_id.id)
        user_serializer = UserSerializer(user)
        return user_serializer
    except:
        raise credentials_exception

