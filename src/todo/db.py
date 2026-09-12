from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession,async_sessionmaker,create_async_engine)
from fastapi import Depends
from todo.models import User
import os
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase


load_dotenv()

# what is aiomysql
# sqlalchemy itself cannot directly cannot to mysql so use aiomysql
DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{os.getenv("MYSQL_USERNAME")}:"
    f"{os.getenv("MYSQL_PASSWORD")}@"
    f"{os.getenv("MYSQL_HOST")}/"
    f"{os.getenv("MYSQL_DATABASE")}"
)

#Create engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#Gives access to perform databse function sql
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
    
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)




