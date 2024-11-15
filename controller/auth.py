import uuid
from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import UUID4

from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from modals import User, UserInDB, TokenData
from database.users import UserFunction
from database.recipe import RecipiessFunction as Recipe


SECRET_KEY = "thisisasecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Auth:
    def verify_password(plain_password, hashed_password):
        ''' Verify the password '''
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(password):
        ''' Hash the password '''
        return pwd_context.hash(password)
    
    def get_user(db, username):
        ''' Get user by email '''
        for user in db:
            if user["email"] == username:
                return user
        return None
    
    def get_usr_by_id(user_id: UUID4):
        ''' Get user by id '''
        user = UserFunction.get_user_by_id(user_id)
        return user
    
    def register_user(user: User):
        ''' 
        Register user | Create new user 
        ```json
        {
            'name': 'John Doe',
            'email': 'jhonedoe@gmail.com',
            'password': 'password'
        }
        ```
        '''
        user = UserInDB(**user.dict())
        user.password = Auth.hash_password(user.password)
        created_user = UserFunction.create_user(user)
        return created_user
    
    def authenticate_user(username: str, password: str):
        ''' Authenticate user '''
        user = UserFunction.get_user_by_email(email=username)
        
        if not user:
            return False
        if not Auth.verify_password(password, user.password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        ''' Create access token for user when they login '''
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    

    def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        ''' Get current user object '''
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        
        user = UserFunction.get_user_by_email(email=token_data.username)
        
        if user is None:
            raise credentials_exception
        return user


def is_owner_of_recipe(function):
    ''' Decorator to check if user is owner of recipe '''
    def wrapper(*args, **kwargs):
        user = Auth.get_current_user(kwargs["Token"])
        recipe = Recipe.get_recipe_by_id(kwargs["recipe_id"])
        
        if recipe["owner_id"] != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return function(*args, **kwargs)
    return wrapper