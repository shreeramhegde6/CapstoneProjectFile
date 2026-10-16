from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select
from cloudguard.api import router
from cloudguard.config import get_settings
from cloudguard.database import Base, SessionLocal, engine
from cloudguard.models import User
from cloudguard.security import hash_password
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        s=get_settings()
        if not db.scalar(select(User).where(User.username==s.default_admin_username)):
            db.add(User(username=s.default_admin_username,password_hash=hash_password(s.default_admin_password),role="admin")); db.commit()
    yield
app=FastAPI(title="CloudGuard API",version="0.1.0",lifespan=lifespan)
app.include_router(router)
