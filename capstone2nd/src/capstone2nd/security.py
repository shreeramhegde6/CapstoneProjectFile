from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from cloudguard.config import get_settings
from cloudguard.database import get_db
from cloudguard.models import User
pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def hash_password(v): return pwd.hash(v)
def verify_password(v,h): return pwd.verify(v,h)
def create_token(user:User):
    s=get_settings(); exp=datetime.now(timezone.utc)+timedelta(minutes=s.access_token_minutes)
    return jwt.encode({"sub":str(user.id),"role":user.role,"exp":exp},s.jwt_secret,algorithm="HS256")
def current_user(token:str=Depends(oauth2),db:Session=Depends(get_db)):
    try: uid=int(jwt.decode(token,get_settings().jwt_secret,algorithms=["HS256"])["sub"])
    except (JWTError,KeyError,ValueError): raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid token")
    user=db.get(User,uid)
    if not user or not user.is_active: raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Inactive user")
    return user
def require_roles(*roles):
    def dep(user:User=Depends(current_user)):
        if user.role not in roles: raise HTTPException(status.HTTP_403_FORBIDDEN,"Insufficient role")
        return user
    return dep
