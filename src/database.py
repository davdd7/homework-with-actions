from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=True)

# noinspection PyTypeChecker
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
